from pathlib import Path
import os
import yaml

def repo_root():
    return Path(__file__).resolve().parents[3]

def deep_merge(base, override):
    out = dict(base)
    for key, value in (override or {}).items():
        if isinstance(value, dict) and isinstance(out.get(key), dict):
            out[key] = deep_merge(out[key], value)
        else:
            out[key] = value
    return out

def load_yaml(path):
    p = Path(path)
    if not p.exists():
        return {}
    return yaml.safe_load(p.read_text(encoding="utf-8")) or {}

def load_config(config_name=None, config_dir=None):
    config_dir = Path(config_dir) if config_dir else repo_root() / "configs"
    config = {}
    for name in ("project", "paths"):
        config = deep_merge(config, load_yaml(config_dir / f"{name}.yaml"))
    if config_name:
        name = config_name if str(config_name).endswith(".yaml") else f"{config_name}.yaml"
        path = Path(name)
        config = deep_merge(config, load_yaml(path if path.exists() else config_dir / name))
    if os.getenv("BTC_QUANT_PROJECT_ROOT"):
        config["project_root"] = os.environ["BTC_QUANT_PROJECT_ROOT"]
    return config

