import pandas as pd
import numpy as np

def detect_liquidity_sweeps(df: pd.DataFrame) -> pd.DataFrame:
    """Computes liquidity levels and detects sweeps of key highs and lows.
    
    A liquidity sweep occurs when the price wicks past a key level (like a rolling high/low)
    but closes back within the range.
    """
    res = df.copy()
    
    # 1. Rolling highs/lows as liquidity pools
    res["rolling_high_24h"] = res["high"].rolling(288).max() # 24h for 5m candles
    res["rolling_low_24h"] = res["low"].rolling(288).min()
    
    # 2. Equal Highs / Lows (EQH / EQL)
    # Check if current high is within 0.1% of the last swing high
    # We can approximate this by comparing local peaks
    
    # 3. Sweeps detection
    # Bullish sweep: low wicks below rolling_low_24h of the previous bar, but close is above it
    res["bullish_sweep_24h"] = (res["low"] < res["rolling_low_24h"].shift(1)) & (res["close"] > res["rolling_low_24h"].shift(1))
    
    # Bearish sweep: high wicks above rolling_high_24h of the previous bar, but close is below it
    res["bearish_sweep_24h"] = (res["high"] > res["rolling_high_24h"].shift(1)) & (res["close"] < res["rolling_high_24h"].shift(1))
    
    # Calculate wick depth of the sweep
    res["sweep_wick_depth"] = np.where(
        res["bullish_sweep_24h"], 
        res["rolling_low_24h"].shift(1) - res["low"],
        np.where(
            res["bearish_sweep_24h"],
            res["high"] - res["rolling_high_24h"].shift(1),
            0.0
        )
    )
    
    return res
