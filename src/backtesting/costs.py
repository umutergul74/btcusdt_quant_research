import pandas as pd
from typing import Dict, Any

def calculate_costs(
    position_size: float, 
    entry_price: float, 
    exit_price: float, 
    fee_rate: float = 0.0005, 
    slippage_rate: float = 0.0002
) -> Dict[str, float]:
    """Calculates execution costs for a trade.
    
    - fee_rate: 0.0005 (0.05% taker fee)
    - slippage_rate: 0.0002 (0.02% slippage on entry and exit)
    """
    # Size in USD
    trade_value_entry = position_size * entry_price
    trade_value_exit = position_size * exit_price
    
    entry_fee = trade_value_entry * fee_rate
    exit_fee = trade_value_exit * fee_rate
    
    entry_slippage = trade_value_entry * slippage_rate
    exit_slippage = trade_value_exit * slippage_rate
    
    total_costs = entry_fee + exit_fee + entry_slippage + exit_slippage
    
    return {
        "entry_fee": entry_fee,
        "exit_fee": exit_fee,
        "entry_slippage": entry_slippage,
        "exit_slippage": exit_slippage,
        "total_costs": total_costs
    }
