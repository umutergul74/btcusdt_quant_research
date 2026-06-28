import pandas as pd
import numpy as np

def compute_forward_returns(df: pd.DataFrame, horizon: int = 12) -> pd.Series:
    """Computes the forward return over a specified number of bars."""
    return df["close"].shift(-horizon) / df["close"] - 1.0

def generate_return_labels(df: pd.DataFrame, horizon: int = 12, threshold_mult: float = 1.0) -> pd.Series:
    """Generates volatility-adjusted return labels.
    
    Returns:
    - +1: long edge (forward return > threshold)
    - -1: short edge (forward return < -threshold)
    - 0: no edge
    """
    fwd_ret = compute_forward_returns(df, horizon)
    
    # Calculate rolling volatility as threshold
    vol = df["close"].pct_change().rolling(100).std() * np.sqrt(horizon)
    threshold = vol * threshold_mult
    
    labels = pd.Series(0, index=df.index)
    labels = np.where(fwd_ret > threshold, 1, np.where(fwd_ret < -threshold, -1, 0))
    
    # Keep NaNs at the end of the series where forward returns cannot be calculated
    labels = pd.Series(labels, index=df.index)
    labels.iloc[-horizon:] = np.nan
    
    return labels
