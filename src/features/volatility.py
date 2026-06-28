import numpy as np
import pandas as pd

def compute_volatility_features(df: pd.DataFrame, window: int = 14) -> pd.DataFrame:
    """Computes various volatility measures: ATR, Parkinson, and Garman-Klass volatility."""
    res = df.copy()
    
    high, low, close, open_val = res["high"], res["low"], res["close"], res["open"]
    
    # 1. ATR
    tr = pd.concat([high - low, (high - close.shift(1)).abs(), (low - close.shift(1)).abs()], axis=1).max(axis=1)
    res["atr"] = tr.rolling(window).mean()
    res["atr_pct"] = res["atr"] / close
    
    # 2. Parkinson Volatility
    # Parkinson = sqrt( (1 / (4 * ln(2))) * sum( ln(high/low)^2 ) )
    log_hl = np.log(high / low.replace(0, 1e-6))
    parkinson = np.sqrt((log_hl ** 2) / (4 * np.log(2)))
    res["volatility_parkinson"] = parkinson.rolling(window).mean()
    
    # 3. Garman-Klass Volatility
    # GK = sqrt( 0.5 * ln(high/low)^2 - (2 * ln(2) - 1) * ln(close/open)^2 )
    log_co = np.log(close / open_val.replace(0, 1e-6))
    gk = np.sqrt(0.5 * (log_hl ** 2) - (2 * np.log(2) - 1) * (log_co ** 2))
    res["volatility_gk"] = gk.rolling(window).mean()
    
    # 4. Volatility regime: Bollinger Bandwidth
    rolling_mean = close.rolling(20).mean()
    rolling_std = close.rolling(20).std()
    res["bb_bandwidth"] = (rolling_std * 4) / rolling_mean
    res["volatility_compression"] = res["bb_bandwidth"] < res["bb_bandwidth"].rolling(100).quantile(0.2)
    res["volatility_expansion"] = res["bb_bandwidth"] > res["bb_bandwidth"].rolling(100).quantile(0.8)
    
    return res
