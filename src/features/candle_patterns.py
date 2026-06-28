import pandas as pd
import numpy as np

def compute_candle_features(df: pd.DataFrame) -> pd.DataFrame:
    """Computes candle-specific patterns and quality metrics."""
    res = df.copy()
    
    high, low, open_val, close = res["high"], res["low"], res["open"], res["close"]
    
    # 1. Candle dimensions
    res["candle_range"] = high - low
    res["candle_body"] = (close - open_val).abs()
    res["body_range_ratio"] = res["candle_body"] / res["candle_range"].replace(0, 1e-6)
    
    # 2. Wicks
    res["upper_wick"] = np.where(close > open_val, high - close, high - open_val)
    res["lower_wick"] = np.where(close > open_val, open_val - low, close - low)
    res["upper_wick_ratio"] = res["upper_wick"] / res["candle_range"].replace(0, 1e-6)
    res["lower_wick_ratio"] = res["lower_wick"] / res["candle_range"].replace(0, 1e-6)
    
    # 3. Close Location Value (CLV)
    res["clv"] = ((close - low) - (high - close)) / res["candle_range"].replace(0, 1e-6)
    
    # 4. Volume metrics
    res["volume_ma_20"] = res["volume"].rolling(20).mean()
    res["volume_spike"] = res["volume"] > (2 * res["volume_ma_20"])
    
    return res
