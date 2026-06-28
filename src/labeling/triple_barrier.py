import pandas as pd
import numpy as np
from typing import Optional

def apply_triple_barrier(
    df: pd.DataFrame,
    events: pd.Index,
    tp_mult: float = 2.0,
    sl_mult: float = 1.0,
    time_barrier: int = 24,
    atr_col: str = "atr"
) -> pd.DataFrame:
    """Applies the Triple-Barrier Method to a set of event timestamps.
    
    For each event:
    - Upper barrier (TP): entry_price * (1 + tp_mult * ATR_pct)
    - Lower barrier (SL): entry_price * (1 - sl_mult * ATR_pct)
    - Vertical barrier (Time): exit after time_barrier candles
    
    Returns a DataFrame with columns:
    - 'tp_hit': timestamp or index when TP was hit
    - 'sl_hit': timestamp or index when SL was hit
    - 'label': +1 (TP hit first), -1 (SL hit first), 0 (time barrier hit first)
    """
    close = df["close"]
    atr = df[atr_col] if atr_col in df else close.pct_change().rolling(14).std() * close
    
    out = pd.DataFrame(index=events, columns=["tp_hit", "sl_hit", "label"])
    
    for loc in events:
        if loc not in df.index:
            continue
            
        idx = df.index.get_loc(loc)
        if idx + 1 >= len(df):
            continue
            
        entry_price = close.iloc[idx]
        atr_val = atr.iloc[idx]
        
        # Calculate barrier price levels
        tp_price = entry_price + (tp_mult * atr_val)
        sl_price = entry_price - (sl_mult * atr_val)
        
        # Determine expiration index
        exit_idx = min(idx + time_barrier, len(df) - 1)
        
        # Sub-slice of close prices during the trade holding period
        holding_period = close.iloc[idx + 1: exit_idx + 1]
        
        if holding_period.empty:
            continue
            
        # Find first touch of TP or SL
        tp_touches = holding_period[holding_period >= tp_price]
        sl_touches = holding_period[holding_period <= sl_price]
        
        first_tp = tp_touches.index[0] if not tp_touches.empty else None
        first_sl = sl_touches.index[0] if not sl_touches.empty else None
        
        out.at[loc, "tp_hit"] = first_tp
        out.at[loc, "sl_hit"] = first_sl
        
        if first_tp is not None and first_sl is not None:
            # Both hit; check which one was hit first
            if first_tp < first_sl:
                out.at[loc, "label"] = 1
            else:
                out.at[loc, "label"] = -1
        elif first_tp is not None:
            out.at[loc, "label"] = 1
        elif first_sl is not None:
            out.at[loc, "label"] = -1
        else:
            out.at[loc, "label"] = 0
            
    return out
