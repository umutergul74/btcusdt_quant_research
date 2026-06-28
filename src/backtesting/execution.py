import pandas as pd
import numpy as np
from typing import List, Dict, Any
from .costs import calculate_costs

def run_backtest(
    df: pd.DataFrame, 
    signals: pd.Series, 
    tp_mult: float = 2.0, 
    sl_mult: float = 1.0, 
    time_barrier: int = 24,
    fee_rate: float = 0.0005,
    slippage_rate: float = 0.0002
) -> List[Dict[str, Any]]:
    """Simulates trading execution on a price series.
    
    - signals: Series aligned with df index, containing +1 (long), -1 (short), 0 (no trade).
    - Executes at the OPEN of the next candle after the signal is generated.
    """
    trades = []
    in_position = False
    position_type = 0  # +1 for long, -1 for short
    entry_price = 0.0
    entry_time = None
    tp_price = 0.0
    sl_price = 0.0
    
    close = df["close"]
    open_val = df["open"]
    high = df["high"]
    low = df["low"]
    atr = df["atr"] if "atr" in df else close.pct_change().rolling(14).std() * close
    
    for idx in range(len(df) - 1):
        current_time = df.index[idx]
        signal = signals.iloc[idx]
        
        # Check exits if in position
        if in_position:
            holding_bars = df.index.get_loc(df.index[idx]) - df.index.get_loc(entry_time)
            
            # Check Stop Loss & Take Profit
            # In long position
            if position_type == 1:
                # Conservative assumption: if both hit, assume SL hit
                if low.iloc[idx] <= sl_price:
                    exit_price = sl_price
                    exit_reason = "SL"
                    in_position = False
                elif high.iloc[idx] >= tp_price:
                    exit_price = tp_price
                    exit_reason = "TP"
                    in_position = False
                elif holding_bars >= time_barrier:
                    exit_price = close.iloc[idx]
                    exit_reason = "Time"
                    in_position = False
            # In short position
            elif position_type == -1:
                if high.iloc[idx] >= sl_price:
                    exit_price = sl_price
                    exit_reason = "SL"
                    in_position = False
                elif low.iloc[idx] <= tp_price:
                    exit_price = tp_price
                    exit_reason = "TP"
                    in_position = False
                elif holding_bars >= time_barrier:
                    exit_price = close.iloc[idx]
                    exit_reason = "Time"
                    in_position = False
                    
            if not in_position:
                # Calculate trade metrics
                gross_pnl = (exit_price - entry_price) / entry_price if position_type == 1 else (entry_price - exit_price) / entry_price
                
                # Apply costs
                costs = calculate_costs(1.0, entry_price, exit_price, fee_rate, slippage_rate)
                net_pnl = gross_pnl - (costs["total_costs"] / entry_price)
                
                trades.append({
                    "entry_time": entry_time,
                    "exit_time": current_time,
                    "direction": "LONG" if position_type == 1 else "SHORT",
                    "entry_price": entry_price,
                    "exit_price": exit_price,
                    "exit_reason": exit_reason,
                    "gross_pnl": gross_pnl,
                    "net_pnl": net_pnl,
                    "holding_bars": holding_bars
                })
                
        # Check entry (only if not in position)
        if not in_position and signal in [1, -1]:
            in_position = True
            position_type = signal
            # Execute at the open of the next candle
            entry_price = open_val.iloc[idx + 1]
            entry_time = df.index[idx + 1]
            atr_val = atr.iloc[idx]
            
            if position_type == 1:
                tp_price = entry_price + (tp_mult * atr_val)
                sl_price = entry_price - (sl_mult * atr_val)
            else:
                tp_price = entry_price - (tp_mult * atr_val)
                sl_price = entry_price + (sl_mult * atr_val)
                
    return trades
