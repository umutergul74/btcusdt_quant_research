import numpy as np

def calculate_fixed_fractional_size(
    capital: float, 
    risk_pct: float, 
    entry_price: float, 
    stop_price: float
) -> float:
    """Calculates trade size based on the fixed fractional risk method.
    
    Size = (Capital * Risk%) / (Entry Price - Stop Price)
    """
    risk_amount = capital * risk_pct
    price_risk = abs(entry_price - stop_price)
    
    if price_risk == 0:
        return 0.0
        
    size_units = risk_amount / price_risk
    return size_units

def calculate_kelly_size(
    capital: float, 
    win_rate: float, 
    payoff_ratio: float, 
    fraction_cap: float = 0.25
) -> float:
    """Calculates position size using the Kelly Criterion with a fraction cap.
    
    Kelly % = Win Rate - (1 - Win Rate) / Payoff Ratio
    """
    if payoff_ratio <= 0:
        return 0.0
        
    kelly_pct = win_rate - ((1.0 - win_rate) / payoff_ratio)
    # Apply fractional Kelly and cap it
    final_pct = max(0.0, min(kelly_pct * fraction_cap, fraction_cap))
    return capital * final_pct
