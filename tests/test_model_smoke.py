from btc_quant.pipeline.stages import run_stage

def test_debug_pipeline_smoke(tmp_path):
    stages = ["data_ohlcv", "data_quality", "build_features", "build_labels", "build_research_dataset", "train_baselines", "train_tabular", "calibrate_models", "validate_walk_forward", "run_falsification", "run_drift_checks", "evaluate_phase1_gate", "package_phase1_performance"]
    for stage in stages:
        result = run_stage(stage, project_root=tmp_path, run_id="pytest_debug")
        assert result["stage"] == stage
    assert (tmp_path / "reports" / "experiments" / "pytest_debug" / "phase1_performance_bundle_pytest_debug.zip").exists()

