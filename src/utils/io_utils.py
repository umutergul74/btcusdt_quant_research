import os
import json
import joblib
import pandas as pd
from typing import Any, Optional

def save_parquet(df: pd.DataFrame, path: str, logger: Optional[Any] = None) -> bool:
    """Saves a pandas DataFrame to a Parquet file safely, creating parent directories."""
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        df.to_parquet(path, index=True)
        if logger:
            logger.info(f"Successfully saved DataFrame to {path} (shape: {df.shape})")
        return True
    except Exception as e:
        if logger:
            logger.error(f"Failed to save Parquet to {path}: {e}")
        else:
            print(f"Failed to save Parquet to {path}: {e}")
        return False

def load_parquet(path: str, logger: Optional[Any] = None) -> Optional[pd.DataFrame]:
    """Loads a pandas DataFrame from a Parquet file safely."""
    if not os.path.exists(path):
        if logger:
            logger.warning(f"Parquet file not found: {path}")
        return None
    try:
        df = pd.read_parquet(path)
        if logger:
            logger.info(f"Successfully loaded DataFrame from {path} (shape: {df.shape})")
        return df
    except Exception as e:
        if logger:
            logger.error(f"Failed to load Parquet from {path}: {e}")
        else:
            print(f"Failed to load Parquet from {path}: {e}")
        return None

def save_json(data: Any, path: str, logger: Optional[Any] = None) -> bool:
    """Saves data to a JSON file safely."""
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            json.dump(data, f, indent=4)
        if logger:
            logger.info(f"Successfully saved JSON to {path}")
        return True
    except Exception as e:
        if logger:
            logger.error(f"Failed to save JSON to {path}: {e}")
        return False

def load_json(path: str, logger: Optional[Any] = None) -> Optional[Any]:
    """Loads data from a JSON file safely."""
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r") as f:
            data = json.load(f)
        return data
    except Exception as e:
        if logger:
            logger.error(f"Failed to load JSON from {path}: {e}")
        return None

def save_model(model: Any, path: str, logger: Optional[Any] = None) -> bool:
    """Saves a model object using joblib safely."""
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        joblib.dump(model, path)
        if logger:
            logger.info(f"Successfully saved model to {path}")
        return True
    except Exception as e:
        if logger:
            logger.error(f"Failed to save model to {path}: {e}")
        return False

def load_model(path: str, logger: Optional[Any] = None) -> Optional[Any]:
    """Loads a model object using joblib safely."""
    if not os.path.exists(path):
        return None
    try:
        model = joblib.load(path)
        if logger:
            logger.info(f"Successfully loaded model from {path}")
        return model
    except Exception as e:
        if logger:
            logger.error(f"Failed to load model from {path}: {e}")
        return None
