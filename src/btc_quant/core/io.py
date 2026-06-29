from pathlib import Path
import json
import tempfile
import pandas as pd
import yaml

def ensure_dir(path):
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p

def atomic_write_text(path, text):
    path = Path(path)
    ensure_dir(path.parent)
    with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8", dir=str(path.parent)) as tmp:
        tmp.write(text)
        tmp_path = Path(tmp.name)
    tmp_path.replace(path)
    return path

def write_json(path, data):
    return atomic_write_text(path, json.dumps(data, indent=2, default=str) + "\n")

def read_json(path, default=None):
    p = Path(path)
    if not p.exists():
        return default
    return json.loads(p.read_text(encoding="utf-8"))

def write_yaml(path, data):
    return atomic_write_text(path, yaml.safe_dump(data, sort_keys=False))

def read_yaml(path, default=None):
    p = Path(path)
    if not p.exists():
        return default
    value = yaml.safe_load(p.read_text(encoding="utf-8"))
    return default if value is None else value

def write_frame(path, frame):
    path = Path(path)
    ensure_dir(path.parent)
    if path.suffix == ".parquet":
        try:
            frame.to_parquet(path, index=False)
            return path
        except Exception:
            fallback = path.with_suffix(".csv")
            frame.to_csv(fallback, index=False)
            write_json(path.with_suffix(".parquet.fallback.json"), {"actual": str(fallback)})
            return fallback
    frame.to_csv(path, index=False)
    return path

def read_frame(path):
    path = Path(path)
    if path.exists():
        if path.suffix == ".parquet":
            return pd.read_parquet(path)
        return pd.read_csv(path)
    meta = path.with_suffix(".parquet.fallback.json")
    if meta.exists():
        return pd.read_csv(read_json(meta)["actual"])
    raise FileNotFoundError(path)

