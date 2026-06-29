import json
import pandas as pd
from btc_quant.core.exceptions import Phase2BlockedError
from btc_quant.core.io import read_frame, write_frame, write_json, atomic_write_text
from btc_quant.data.cleaning import clean_ohlcv
from btc_quant.data.downloader import create_synthetic_ohlcv
from btc_quant.data.quality import validate_ohlcv
from btc_quant.features.registry import build_features as make_features
from btc_quant.features.matrix_builder import build_xy
from btc_quant.features.quality import feature_quality_summary
from btc_quant.labels.forward_returns import build_forward_return_labels
from btc_quant.labels.quality import label_quality_summary
from btc_quant.models.baselines import evaluate_baselines
from btc_quant.models.calibration import brier_score_binary, expected_calibration_error
from btc_quant.models.tabular import train_tabular_models
from btc_quant.performance.bundle import build_phase1_bundle
from btc_quant.pipeline.run_context import create_run_context
from btc_quant.pipeline.stage_registry import get_stage_spec
from btc_quant.validation.gate import evaluate_phase1_gate as gate_decision
from btc_quant.validation.leakage import check_feature_availability
from btc_quant.validation.metrics import classification_summary
from btc_quant.validation.splits import chronological_train_test_split
from btc_quant.validation.walk_forward import run_walk_forward

def _paths(ctx):
    return {
        "ohlcv": ctx.paths.processed / "ohlcv_5m.parquet",
        "features": ctx.paths.feature_store / "features_5m.parquet",
        "labels": ctx.paths.labels / "labels_5m.parquet",
        "dataset": ctx.paths.processed / "research_dataset.parquet",
    }

def _record(ctx, stage, result):
    payload = {"stage": stage, "run_id": ctx.run_id, **result}
    write_json(ctx.experiment_dir / f"stage_{stage}.json", payload)
    return payload

def _bootstrap(ctx):
    ctx.paths.mkdirs()
    return {"status": "PASS", "project_root": str(ctx.project_root)}

def _sync_repo(ctx):
    return {"status": "SKIPPED", "reason": "GitHub publishing is local workflow, not a Phase 1 notebook."}

def _data_ohlcv(ctx):
    p = _paths(ctx)["ohlcv"]
    rows = int(ctx.config.get("synthetic_debug_rows", 1500))
    frame = clean_ohlcv(create_synthetic_ohlcv(rows=rows, seed=int(ctx.config.get("random_seed", 42))))
    actual = write_frame(p, frame)
    return {"status": "PASS", "rows": int(len(frame)), "output": str(actual)}

def _data_quality(ctx):
    result = validate_ohlcv(read_frame(_paths(ctx)["ohlcv"]))
    write_json(ctx.experiment_dir / "data_quality_summary.json", result)
    return result

def _build_features(ctx):
    features = make_features(read_frame(_paths(ctx)["ohlcv"]))
    actual = write_frame(_paths(ctx)["features"], features)
    write_json(ctx.experiment_dir / "feature_summary.json", feature_quality_summary(features))
    leakage = check_feature_availability(features)
    write_json(ctx.experiment_dir / "leakage_report.json", leakage)
    return {"status": leakage["status"], "rows": int(len(features)), "output": str(actual)}

def _build_labels(ctx):
    labels = build_forward_return_labels(read_frame(_paths(ctx)["ohlcv"]))
    actual = write_frame(_paths(ctx)["labels"], labels)
    summary = label_quality_summary(labels)
    write_json(ctx.experiment_dir / "label_summary.json", summary)
    return {"status": summary["status"], "rows": int(len(labels)), "output": str(actual)}

def _build_research_dataset(ctx):
    features = read_frame(_paths(ctx)["features"])
    labels = read_frame(_paths(ctx)["labels"])
    features["bar_close_time"] = pd.to_datetime(features["bar_close_time"], utc=True)
    features["decision_time"] = pd.to_datetime(features["decision_time"], utc=True)
    labels["bar_close_time"] = pd.to_datetime(labels["bar_close_time"], utc=True)
    labels["decision_time"] = pd.to_datetime(labels["decision_time"], utc=True)
    dataset = features.merge(labels, on=["bar_close_time", "decision_time"], how="inner")
    actual = write_frame(_paths(ctx)["dataset"], dataset)
    return {"status": "PASS", "rows": int(len(dataset)), "output": str(actual)}

def _train_baselines(ctx):
    _, y, _, _ = build_xy(read_frame(_paths(ctx)["dataset"]))
    board = evaluate_baselines(y)
    path = ctx.experiment_dir / "baseline_comparison.csv"
    board.to_csv(path, index=False)
    return {"status": "PASS", "rows": int(len(board)), "output": str(path)}

def _train_tabular(ctx):
    X, y, cols, _ = build_xy(read_frame(_paths(ctx)["dataset"]))
    train_idx, test_idx = chronological_train_test_split(len(X), 0.2)
    models = train_tabular_models(X.iloc[train_idx], y.iloc[train_idx], enabled=ctx.config.get("models", {}))
    rows = []
    pred_rows = []
    for model in models:
        pred = model.estimator.predict(X.iloc[test_idx])
        metrics = classification_summary(y.iloc[test_idx], pred)
        metrics.update({"model": model.name, "train_rows": int(len(train_idx)), "test_rows": int(len(test_idx))})
        rows.append(metrics)
        pred_rows.append(pd.DataFrame({"model": model.name, "predicted_class": pred, "target": y.iloc[test_idx].to_numpy()}))
    leaderboard = pd.DataFrame(rows).sort_values("macro_f1", ascending=False)
    leaderboard.to_csv(ctx.experiment_dir / "model_leaderboard.csv", index=False)
    pd.concat(pred_rows, ignore_index=True).to_csv(ctx.experiment_dir / "predictions_summary.csv", index=False)
    write_json(ctx.experiment_dir / "feature_list.json", {"feature_columns": cols})
    atomic_write_text(ctx.experiment_dir / "model_card.md", "# Phase 1 Model Card\n\nNo formal backtest included.\n")
    return {"status": "PASS", "models": [m.name for m in models]}

def _calibrate_models(ctx):
    preds = pd.read_csv(ctx.experiment_dir / "predictions_summary.csv")
    prob_long = (preds["predicted_class"] == 1).astype(float)
    result = {"status": "YELLOW", "brier_score_long_indicator": brier_score_binary(preds["target"], prob_long), "ece_long_indicator": expected_calibration_error(preds["target"], prob_long)}
    write_json(ctx.experiment_dir / "calibration_report.json", result)
    pd.DataFrame([result]).to_csv(ctx.experiment_dir / "calibration_metrics.csv", index=False)
    return result

def _validate_walk_forward(ctx):
    X, y, _, _ = build_xy(read_frame(_paths(ctx)["dataset"]))
    folds = run_walk_forward(X, y, model_config=ctx.config, min_folds=3)
    folds.to_csv(ctx.experiment_dir / "fold_metrics.csv", index=False)
    return {"status": "PASS" if len(folds) else "FAIL", "fold_rows": int(len(folds))}

def _run_falsification(ctx):
    result = {"status": "YELLOW", "random_label_sanity": "not_run_in_skeleton", "shuffled_feature_sanity": "not_run_in_skeleton"}
    write_json(ctx.experiment_dir / "robustness_checks.json", result)
    return result

def _run_drift_checks(ctx):
    result = {"status": "YELLOW", "rows": int(len(read_frame(_paths(ctx)["dataset"])))}
    write_json(ctx.experiment_dir / "drift_report.json", result)
    return result

def _evaluate_phase1_gate(ctx):
    def load(name):
        path = ctx.experiment_dir / name
        return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    checks = {
        "data_quality": load("data_quality_summary.json").get("status") == "PASS",
        "label_quality": load("label_summary.json").get("status") == "PASS",
        "no_leakage": load("leakage_report.json").get("status") == "PASS",
        "walk_forward_positive": (ctx.experiment_dir / "fold_metrics.csv").exists(),
        "calibration_report": (ctx.experiment_dir / "calibration_report.json").exists(),
        "baseline_improvement": False,
        "falsification_pass": False,
    }
    decision = gate_decision(checks)
    write_json(ctx.experiment_dir / "decision_report.json", decision)
    atomic_write_text(ctx.experiment_dir / "gate_decision.md", f"# Phase 1 Gate\n\nStatus: `{decision['gate_status']}`\n\nPhase 2 allowed: `false`\n")
    return decision

def _package_phase1_performance(ctx):
    zip_path = build_phase1_bundle(ctx.experiment_dir, ctx.run_id)
    return {"status": "PASS", "zip_path": str(zip_path)}

def _generate_phase1_reports(ctx):
    atomic_write_text(ctx.experiment_dir / "next_actions_for_codex.md", "# Next Actions\n\nContinue Phase 1 model improvement. Phase 2 remains blocked.\n")
    return {"status": "PASS"}

STAGE_FUNCTIONS = {
    "bootstrap": _bootstrap, "sync_repo": _sync_repo, "data_ohlcv": _data_ohlcv,
    "data_quality": _data_quality, "futures_metrics": lambda ctx: {"status": "SKIPPED_LOCAL_DEBUG"},
    "aggtrades_optional": lambda ctx: {"status": "DISABLED_BY_DEFAULT"},
    "build_features": _build_features, "build_labels": _build_labels,
    "build_research_dataset": _build_research_dataset, "train_baselines": _train_baselines,
    "train_tabular": _train_tabular, "calibrate_models": _calibrate_models,
    "validate_walk_forward": _validate_walk_forward, "run_falsification": _run_falsification,
    "run_drift_checks": _run_drift_checks, "evaluate_phase1_gate": _evaluate_phase1_gate,
    "package_phase1_performance": _package_phase1_performance, "generate_phase1_reports": _generate_phase1_reports,
}

def run_stage(stage_name, config_name=None, project_root=None, run_id=None):
    spec = get_stage_spec(stage_name)
    if not spec.allowed_before_phase2_promotion:
        raise Phase2BlockedError(f"{stage_name} is Phase 2 and blocked until promotion_allowed is true.")
    ctx = create_run_context(config_name=config_name, project_root=project_root, run_id=run_id)
    return _record(ctx, stage_name, STAGE_FUNCTIONS[stage_name](ctx))

def run_experiment(config_name, project_root=None, run_id=None):
    ctx = create_run_context(config_name=config_name, project_root=project_root, run_id=run_id)
    results = []
    for stage in ctx.config.get("stages", []):
        results.append(run_stage(stage, config_name=config_name, project_root=ctx.project_root, run_id=ctx.run_id))
    return results

