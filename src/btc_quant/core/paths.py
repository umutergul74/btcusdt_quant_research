from dataclasses import dataclass
from pathlib import Path
import os

@dataclass(frozen=True)
class ProjectPaths:
    project_root: Path
    data: Path
    raw: Path
    processed: Path
    feature_store: Path
    labels: Path
    events: Path
    models: Path
    reports: Path
    experiments: Path
    logs: Path
    cache: Path

    @classmethod
    def from_root(cls, root):
        root = Path(root)
        return cls(root, root/"data", root/"data/raw", root/"data/processed",
                   root/"data/feature_store", root/"data/labels", root/"data/events",
                   root/"models", root/"reports", root/"reports/experiments",
                   root/"logs", root/"cache")

    def mkdirs(self):
        for value in self.__dict__.values():
            if isinstance(value, Path):
                value.mkdir(parents=True, exist_ok=True)

def resolve_project_root(project_root=None, config=None):
    if project_root:
        return Path(project_root)
    if os.getenv("BTC_QUANT_PROJECT_ROOT"):
        return Path(os.environ["BTC_QUANT_PROJECT_ROOT"])
    if config and config.get("project_root") and Path(config["project_root"]).exists():
        return Path(config["project_root"])
    return Path.cwd()

