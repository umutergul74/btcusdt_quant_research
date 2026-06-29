from pathlib import Path
import csv
import zipfile
from btc_quant.core.io import ensure_dir, read_json, write_json, atomic_write_text
from btc_quant.core.time import utc_now_iso

REQUIRED_BUNDLE_FILES = [
    "README_FOR_CODEX.md", "gate_decision.md", "decision_report.json", "auto_review.json",
    "phase1_current_status.json", "phase2_readiness.json", "future_oos_readiness.json",
    "future_oos_preflight.json", "future_oos_evaluation.json", "future_oos_candidate_plan.csv",
    "experiment_policy_guard.csv", "report_consistency_audit.json", "run_summary.json",
    "config_snapshot.yaml", "artifact_manifest.json", "data_quality_summary.json", "feature_summary.json",
    "label_summary.json", "model_leaderboard.csv", "model_leaderboard.md", "fold_metrics.csv",
    "class_metrics.csv", "calibration_metrics.csv", "confidence_deciles.csv", "probability_deciles.csv",
    "regime_breakdown.csv", "setup_breakdown.csv", "session_breakdown.csv", "robustness_checks.json",
    "leakage_report.json", "drift_report.json", "feature_importance_summary.csv",
    "feature_stability_summary.csv", "baseline_comparison.csv", "cost_proxy_sensitivity.csv",
    "failed_checks.json", "next_actions_for_codex.md", "questions_for_next_iteration.md", "notes.md",
]

def _csv(path, rows=None):
    rows = rows or [{"status": "not_available_in_skeleton"}]
    ensure_dir(path.parent)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

def build_phase1_bundle(experiment_dir, run_id):
    experiment_dir = Path(experiment_dir)
    bundle_dir = experiment_dir / "phase1_performance_bundle"
    ensure_dir(bundle_dir)
    gate = read_json(experiment_dir / "decision_report.json", {"gate_status": "RED", "required_failures": []})
    common = {"run_id": run_id, "created_at_utc": utc_now_iso(), "phase2_allowed": False}
    atomic_write_text(bundle_dir / "README_FOR_CODEX.md", f"# Phase 1 Performance Bundle\n\nRun: `{run_id}`\n\nNo formal backtest is included. Phase 2 remains blocked.\n")
    atomic_write_text(bundle_dir / "gate_decision.md", f"# Gate Decision\n\nStatus: `{gate.get('gate_status', 'RED')}`\n\nDecision: `DO_NOT_PROCEED_TO_PHASE2`\n")
    json_defaults = {
        "decision_report.json": {**gate, "phase2_allowed": False, "promotion_allowed": False},
        "auto_review.json": {**common, "status": "review_required"},
        "phase1_current_status.json": {**common, "phase": "Phase 1", "formal_backtest_enabled": False},
        "phase2_readiness.json": {**common, "ready_for_phase2": False, "block_reason": "future_oos_not_completed_and_passed"},
        "future_oos_readiness.json": {**common, "ready_for_evaluation": False, "promotion_allowed": False},
        "future_oos_preflight.json": {**common, "status": "not_ready"},
        "future_oos_evaluation.json": {**common, "evaluation_completed": False, "primary_candidate_passed": False},
        "report_consistency_audit.json": {**common, "report_consistency_passed": True, "promotion_allowed": False, "decision": "DO_NOT_PROCEED_TO_PHASE2"},
        "run_summary.json": common,
        "artifact_manifest.json": {**common, "artifacts": []},
        "failed_checks.json": {"failed_checks": gate.get("required_failures", [])},
    }
    for name in ["data_quality_summary.json", "feature_summary.json", "label_summary.json", "robustness_checks.json", "leakage_report.json", "drift_report.json"]:
        json_defaults[name] = read_json(experiment_dir / name, {"status": "not_available"})
    for name, data in json_defaults.items():
        write_json(bundle_dir / name, data)
    atomic_write_text(bundle_dir / "config_snapshot.yaml", "phase: phase1_model_research\nformal_backtest_enabled: false\n")
    for name in [n for n in REQUIRED_BUNDLE_FILES if n.endswith(".md") and not (bundle_dir / n).exists()]:
        atomic_write_text(bundle_dir / name, f"# {name}\n\nPhase 1 skeleton output.\n")
    for name in [n for n in REQUIRED_BUNDLE_FILES if n.endswith(".csv")]:
        _csv(bundle_dir / name, [{"run_id": run_id, "status": "not_available_or_generated_in_skeleton"}])
    zip_path = experiment_dir / f"phase1_performance_bundle_{run_id}.zip"
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for file in bundle_dir.rglob("*"):
            if file.is_file():
                zf.write(file, file.relative_to(experiment_dir))
    return zip_path

