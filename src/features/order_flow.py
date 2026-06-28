import pandas as pd
import numpy as np

def compute_order_flow_features(df: pd.DataFrame) -> pd.DataFrame:
    """Computes volume delta and Cumulative Volume Delta (CVD) features.
    
    Uses 'taker_buy_base_volume' (if present in the DataFrame) to calculate volume delta.
    Otherwise, falls back to a proxy based on price action.
    """
    res = df.copy()
    
    # 1. Volume Delta
    if "taker_buy_base_volume" in res and "volume" in res:
        # Taker sell volume = Total volume - Taker buy volume
        taker_buy = res["taker_buy_base_volume"].astype(float)
        total_vol = res["volume"].astype(float)
        taker_sell = total_vol - taker_buy
        res["volume_delta"] = taker_buy - taker_sell
    else:
        # Fallback proxy: Volume * Close Location Value (CLV)
        # CLV = ((Close - Low) - (High - Close)) / (High - Low)
        clv = ((res["close"] - res["low"]) - (res["high"] - res["close"])) / (res["high"] - res["low"]).replace(0, 1e-6)
        res["volume_delta"] = res["volume"] * clv
        
    # 2. Cumulative Volume Delta (CVD)
    res["cvd"] = res["volume_delta"].cumsum()
    
    # 3. CVD rolling slopes
    res["cvd_slope_5"] = res["cvd"].diff(5)
    res["cvd_slope_20"] = res["cvd"].diff(20)
    
    # 4. CVD Divergence
    # Bullish divergence: price makes lower low over last 10 bars, but CVD makes higher low
    price_ll = res["low"] < res["low"].shift(10)
    cvd_hl = res["cvd"] > res["cvd"].shift(10)
    res["bullish_cvd_divergence"] = price_ll & cvd_hl
    
    # Bearish divergence: price makes higher high, but CVD makes lower high
    price_hh = res["high"] > res["high"].shift(10)
    cvd_lh = res["cvd"] < res["cvd"].shift(10)
    res["bearish_cvd_divergence"] = price_hh & cvd_lh
    
    return res
