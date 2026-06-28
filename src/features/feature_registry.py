import os
import json
import pandas as pd
from typing import List, Dict, Any
from utils.logging_utils import setup_logger
from .market_structure import compute_market_structure
from .fvg import detect_fvgs
from .order_blocks import detect_order_blocks
from .liquidity import detect_liquidity_sweeps
from .order_flow import compute_order_flow_features
from .volatility import compute_volatility_features
from .sessions import compute_session_features
from .candle_patterns import compute_candle_features
from .confluence import compute_confluence_score

logger = setup_logger("feature_registry")

FEATURE_METADATA = {
    "confirmed_swing_high": {
        "family": "market_structure",
        "description": "True if candle is a swing high (requires lookahead, shift by window for realtime)",
        "leakage_risk": "High if not shifted"
    },
    "realtime_swing_high": {
        "family": "market_structure",
        "description": "True when a swing high is confirmed in real-time (shifted by window)",
        "leakage_risk": "None"
    },
    "bullish_bos": {
        "family": "market_structure",
        "description": "True if close crosses above last swing high",
        "leakage_risk": "None"
    },
    "bullish_fvg": {
        "family": "fvg",
        "description": "True if a bullish Fair Value Gap is created",
        "leakage_risk": "None"
    },
    "bullish_ob": {
        "family": "order_blocks",
        "description": "True if a bullish Order Block is created",
        "leakage_risk": "None"
    },
    "bullish_sweep_24h": {
        "family": "liquidity",
        "description": "True if low wicks below 24h rolling low and close is above it",
        "leakage_risk": "None"
    },
    "cvd": {
        "family": "order_flow",
        "description": "Cumulative Volume Delta",
        "leakage_risk": "None"
    },
    "volatility_parkinson": {
        "family": "volatility",
        "description": "Parkinson volatility metric",
        "leakage_risk": "None"
    },
    "session_london": {
        "family": "sessions",
        "description": "True if current hour is in London session",
        "leakage_risk": "None"
    },
    "confluence_score": {
        "family": "confluence",
        "description": "Net confluence score (bullish_score - bearish_score)",
        "leakage_risk": "None"
    }
}

def generate_all_features(df: pd.DataFrame) -> pd.DataFrame:
    """Runs the entire feature engineering pipeline on a cleaned DataFrame."""
    logger.info("Starting feature engineering pipeline...")
    
    res = df.copy()
    res = compute_market_structure(res)
    res = detect_fvgs(res)
    res = detect_order_blocks(res)
    res = detect_liquidity_sweeps(res)
    res = compute_order_flow_features(res)
    res = compute_volatility_features(res)
    res = compute_session_features(res)
    res = compute_candle_features(res)
    res = compute_confluence_score(res)
    
    logger.info(f"Feature engineering pipeline completed. Total features: {len(res.columns)}")
    return res

def save_feature_metadata(project_root: str):
    """Saves feature metadata to the feature store directory."""
    path = os.path.join(project_root, "data", "feature_store", "feature_metadata.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(FEATURE_METADATA, f, indent=4)
    logger.info(f"Feature metadata saved to {path}")
