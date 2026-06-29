from dataclasses import dataclass

@dataclass(frozen=True)
class StageSpec:
    name: str
    phase: str
    inputs: list
    outputs: list
    config_dependencies: list
    artifact_manifest_entries: list
    restart_policy: str
    force_rebuild_behavior: str
    expected_runtime_class: str
    leakage_sensitivity_level: str
    validation_checks: list
    failure_behavior: str
    allowed_before_phase2_promotion: bool = True

PHASE1_STAGE_NAMES = ["bootstrap", "sync_repo", "data_ohlcv", "data_quality", "futures_metrics", "aggtrades_optional", "build_features", "build_labels", "build_research_dataset", "train_baselines", "train_tabular", "calibrate_models", "validate_walk_forward", "run_falsification", "run_drift_checks", "evaluate_phase1_gate", "package_phase1_performance", "generate_phase1_reports"]
PHASE2_DISABLED_STAGE_NAMES = ["backtest_phase2_later", "risk_phase2_later", "dashboard_phase2_later"]

def _spec(name, phase="Phase 1", allowed=True):
    return StageSpec(name, phase, [], [], ["project.yaml", "paths.yaml"], [name], "skip_existing_unless_force_rebuild", "overwrite_stage_outputs_only", "medium" if name in {"data_ohlcv", "build_features", "build_labels", "train_tabular", "validate_walk_forward"} else "light", "high" if name in {"build_features", "build_labels", "build_research_dataset", "train_tabular", "validate_walk_forward"} else "medium", ["timestamp_utc", "no_labels_as_features"], "fail_closed_and_report", allowed)

STAGE_REGISTRY = {name: _spec(name) for name in PHASE1_STAGE_NAMES}
for name in PHASE2_DISABLED_STAGE_NAMES:
    STAGE_REGISTRY[name] = _spec(name, "Phase 2", False)

def get_stage_spec(name):
    if name not in STAGE_REGISTRY:
        raise KeyError(f"Unknown stage: {name}")
    return STAGE_REGISTRY[name]

def list_stage_specs():
    return list(STAGE_REGISTRY.values())

