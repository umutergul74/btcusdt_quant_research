from dataclasses import dataclass
from btc_quant.core.config import load_config
from btc_quant.core.paths import ProjectPaths, resolve_project_root
from btc_quant.core.time import utc_now_iso

@dataclass
class RunContext:
    project_root: object
    paths: ProjectPaths
    config: dict
    run_id: str
    experiment_dir: object

def create_run_context(config_name=None, project_root=None, run_id=None):
    config = load_config(config_name)
    root = resolve_project_root(project_root, config)
    paths = ProjectPaths.from_root(root)
    paths.mkdirs()
    rid = run_id or config.get("run_id") or "debug_local"
    experiment_dir = paths.experiments / rid
    experiment_dir.mkdir(parents=True, exist_ok=True)
    config["created_at_utc"] = utc_now_iso()
    return RunContext(root, paths, config, rid, experiment_dir)

