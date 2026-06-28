import os
import json
import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple
from utils.logging_utils import setup_logger

logger = setup_logger("data_cleaning")

def clean_ohlcv(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Cleans OHLCV data and returns the cleaned DataFrame and a quality report."""
    report = {
        "initial_rows": len(df),
        "duplicate_timestamps": 0,
        "missing_timestamps_filled": 0,
        "invalid_ohlc_relations": 0,
        "zero_or_negative_prices": 0,
        "negative_volume": 0,
        "outliers_detected": 0
    }
    
    if df.empty:
        return df, report

    cleaned_df = df.copy()
    
    # 1. Check duplicates
    initial_len = len(cleaned_df)
    cleaned_df = cleaned_df.drop_duplicates(subset=["timestamp"])
    report["duplicate_timestamps"] = initial_len - len(cleaned_df)
    
    # Sort by timestamp
    cleaned_df = cleaned_df.sort_values("timestamp").reset_index(drop=True)
    
    # 2. Check invalid values
    # Prices must be > 0
    price_cols = ["open", "high", "low", "close"]
    for col in price_cols:
        invalid_prices = (cleaned_df[col] <= 0).sum()
        if invalid_prices > 0:
            report["zero_or_negative_prices"] += int(invalid_prices)
            # Fill with NaN to interpolate later
            cleaned_df.loc[cleaned_df[col] <= 0, col] = np.nan

    # Volume must be >= 0
    invalid_vol = (cleaned_df["volume"] < 0).sum()
    if invalid_vol > 0:
        report["negative_volume"] = int(invalid_vol)
        cleaned_df.loc[cleaned_df["volume"] < 0, "volume"] = 0

    # 3. Validate OHLC relationships (high >= open, high >= close, low <= open, low <= close)
    invalid_high = ((cleaned_df["high"] < cleaned_df["open"]) | (cleaned_df["high"] < cleaned_df["close"])).sum()
    invalid_low = ((cleaned_df["low"] > cleaned_df["open"]) | (cleaned_df["low"] > cleaned_df["close"])).sum()
    report["invalid_ohlc_relations"] = int(invalid_high + invalid_low)
    
    if report["invalid_ohlc_relations"] > 0:
        # Correct invalid highs/lows
        cleaned_df["high"] = cleaned_df[["open", "high", "close"]].max(axis=1)
        cleaned_df["low"] = cleaned_df[["open", "low", "close"]].min(axis=1)

    # Interpolate any NaNs created
    cleaned_df[price_cols] = cleaned_df[price_cols].interpolate(method="linear")
    
    # 4. Outliers detection (using rolling Z-score on log returns)
    log_returns = np.log(cleaned_df["close"] / cleaned_df["close"].shift(1))
    z_scores = (log_returns - log_returns.rolling(100).mean()) / log_returns.rolling(100).std()
    outliers = (np.abs(z_scores) > 5).sum()
    report["outliers_detected"] = int(outliers)
    
    report["final_rows"] = len(cleaned_df)
    
    return cleaned_df, report

def save_quality_report(report: Dict[str, Any], path: str):
    """Saves a data quality report to a JSON file."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(report, f, indent=4)
    logger.info(f"Data quality report saved to {path}")
