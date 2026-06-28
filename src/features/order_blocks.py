import pandas as pd
import numpy as np

def detect_order_blocks(df: pd.DataFrame, atr_period: int = 14) -> pd.DataFrame:
    """Computes Order Blocks (OB) and Breaker Blocks features.
    
    A bullish OB is the last bearish candle before a strong bullish move.
    A bearish OB is the last bullish candle before a strong bearish move.
    """
    res = df.copy()
    
    # Calculate ATR
    high, low, close = res["high"], res["low"], res["close"]
    tr = pd.concat([high - low, (high - close.shift(1)).abs(), (low - close.shift(1)).abs()], axis=1).max(axis=1)
    atr = tr.rolling(atr_period).mean()
    
    # Define strong move (displacement)
    # A displacement candle is one where the body is large relative to its ATR
    body = (close - res["open"]).abs()
    displacement = body > (1.5 * atr)
    
    # Bullish OB: Last bearish candle before a bullish displacement
    res["bullish_ob"] = False
    # Bearish OB: Last bullish candle before a bearish displacement
    res["bearish_ob"] = False
    
    for idx in range(2, len(res)):
        # Bullish OB
        if displacement.iloc[idx] and close.iloc[idx] > res["open"].iloc[idx]:
            # Look back to find the last bearish candle
            for lookback in range(1, 5):
                if close.iloc[idx - lookback] < res["open"].iloc[idx - lookback]:
                    res.iloc[idx, res.columns.get_loc("bullish_ob")] = True
                    break
        # Bearish OB
        if displacement.iloc[idx] and close.iloc[idx] < res["open"].iloc[idx]:
            # Look back to find the last bullish candle
            for lookback in range(1, 5):
                if close.iloc[idx - lookback] > res["open"].iloc[idx - lookback]:
                    res.iloc[idx, res.columns.get_loc("bearish_ob")] = True
                    break
                    
    # OB boundaries
    res["ob_top"] = np.where(res["bullish_ob"], res["high"].shift(1), np.where(res["bearish_ob"], res["high"].shift(1), np.nan))
    res["ob_bottom"] = np.where(res["bullish_ob"], res["low"].shift(1), np.where(res["bearish_ob"], res["low"].shift(1), np.nan))
    res["ob_mid"] = (res["ob_top"] + res["ob_bottom"]) / 2
    
    # Forward-fill OB levels to make them available as support/resistance features
    res["last_bullish_ob_top"] = res["ob_top"].where(res["bullish_ob"]).ffill()
    res["last_bullish_ob_bottom"] = res["ob_bottom"].where(res["bullish_ob"]).ffill()
    res["last_bearish_ob_top"] = res["ob_top"].where(res["bearish_ob"]).ffill()
    res["last_bearish_ob_bottom"] = res["ob_bottom"].where(res["bearish_ob"]).ffill()
    
    return res
