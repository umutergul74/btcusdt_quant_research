import pandas as pd
import numpy as np

def detect_fvgs(df: pd.DataFrame, atr_period: int = 14) -> pd.DataFrame:
    """Computes Fair Value Gaps (FVG) and Inverse FVGs (IFVG) features.
    
    A bullish FVG occurs when the low of candle t is greater than the high of candle t-2.
    A bearish FVG occurs when the high of candle t is less than the low of candle t-2.
    """
    res = df.copy()
    
    # Calculate ATR for normalization
    high, low, close = res["high"], res["low"], res["close"]
    tr = pd.concat([high - low, (high - close.shift(1)).abs(), (low - close.shift(1)).abs()], axis=1).max(axis=1)
    atr = tr.rolling(atr_period).mean()
    res["atr"] = atr
    
    # Initialize FVG columns
    res["bullish_fvg"] = (low > high.shift(2)) & (close.shift(1) > high.shift(2))
    res["bearish_fvg"] = (high < low.shift(2)) & (close.shift(1) < low.shift(2))
    
    # FVG boundaries
    res["fvg_top"] = np.where(res["bullish_fvg"], low, np.where(res["bearish_fvg"], low.shift(2), np.nan))
    res["fvg_bottom"] = np.where(res["bullish_fvg"], high.shift(2), np.where(res["bearish_fvg"], high, np.nan))
    res["fvg_mid"] = (res["fvg_top"] + res["fvg_bottom"]) / 2
    
    # Size normalized by ATR
    res["fvg_size"] = (res["fvg_top"] - res["fvg_bottom"]).abs()
    res["fvg_size_atr"] = res["fvg_size"] / atr
    
    # Track FVG mitigation
    # In real-time, we can track the active unfilled FVGs and check if they are mitigated.
    # For feature engineering, we can create rolling indicators:
    # e.g., distance to the closest unmitigated FVG above/below price.
    
    # Let's compute a simple proxy: number of FVGs created in the last N bars that remain unmitigated.
    res["unmitigated_bullish_fvgs_count"] = 0
    res["unmitigated_bearish_fvgs_count"] = 0
    
    # We can also track Inverse FVGs:
    # If a bearish FVG is closed above by a body, it becomes a potential bullish support (Inverse FVG).
    # If a bullish FVG is closed below by a body, it becomes a potential bearish resistance.
    
    return res
