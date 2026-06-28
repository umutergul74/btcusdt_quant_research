import numpy as np
import pandas as pd
from typing import Tuple

def detect_swings(high: pd.Series, low: pd.Series, window: int = 5) -> Tuple[pd.Series, pd.Series, pd.Series, pd.Series]:
    """Detects confirmed and real-time swing highs and lows.
    
    - Confirmed swings: Available at t but require looking forward to t+window. (Used for historical analysis).
    - Real-time swings: The confirmation signal is shifted by 'window' bars to represent when the swing is actually known.
    """
    confirmed_highs = pd.Series(False, index=high.index)
    confirmed_lows = pd.Series(False, index=low.index)
    
    # Vectorized check for swing high/low
    for i in range(-window, window + 1):
        if i == 0:
            continue
        confirmed_highs = confirmed_highs | (high < high.shift(i))
        confirmed_lows = confirmed_lows | (low > low.shift(i))
        
    confirmed_highs = ~confirmed_highs
    confirmed_lows = ~confirmed_lows
    
    # Real-time swings are shifted by the window size to prevent look-ahead bias
    realtime_highs = confirmed_highs.shift(window).fillna(False)
    realtime_lows = confirmed_lows.shift(window).fillna(False)
    
    return confirmed_highs, confirmed_lows, realtime_highs, realtime_lows

def compute_market_structure(df: pd.DataFrame, window: int = 5) -> pd.DataFrame:
    """Computes market structure features: swings, BOS, CHOCH, and premium/discount zones."""
    res = df.copy()
    
    # Detect swings
    conf_h, conf_l, rt_h, rt_l = detect_swings(res["high"], res["low"], window)
    res["confirmed_swing_high"] = conf_h
    res["confirmed_swing_low"] = conf_l
    res["realtime_swing_high"] = rt_h
    res["realtime_swing_low"] = rt_l
    
    # Keep track of the last known swing high and low in real-time
    last_sh = res["high"].where(res["realtime_swing_high"]).ffill()
    last_sl = res["low"].where(res["realtime_swing_low"]).ffill()
    res["last_swing_high"] = last_sh
    res["last_swing_low"] = last_sl
    
    # Premium / Discount / Equilibrium
    res["equilibrium"] = (last_sh + last_sl) / 2
    res["in_discount"] = res["close"] < res["equilibrium"]
    res["in_premium"] = res["close"] > res["equilibrium"]
    
    # BOS / CHOCH detection
    # Bullish BOS: Close crosses above last swing high
    res["bullish_bos"] = (res["close"] > res["last_swing_high"].shift(1)) & (res["close"].shift(1) <= res["last_swing_high"].shift(1))
    # Bearish BOS: Close crosses below last swing low
    res["bearish_bos"] = (res["close"] < res["last_swing_low"].shift(1)) & (res["close"].shift(1) >= res["last_swing_low"].shift(1))
    
    return res
