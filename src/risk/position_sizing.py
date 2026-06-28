import numpy as np

class KellySizer:
    """Calculates position size using the Kelly Criterion."""
    def __init__(self, fractional_kelly: float = 0.5, max_position_size: float = 0.25):
        self.fractional_kelly = fractional_kelly
        self.max_position_size = max_position_size

    def calculate_size(self, p_win: float, win_loss_ratio: float) -> float:
        """Calculates position size percentage based on Kelly Criterion.
        
        Kelly % = Win Rate - (1 - Win Rate) / Payoff Ratio
        """
        if win_loss_ratio <= 0:
            return 0.0
            
        kelly_pct = p_win - ((1.0 - p_win) / win_loss_ratio)
        # Apply fractional Kelly and cap it
        final_pct = max(0.0, min(kelly_pct * self.fractional_kelly, self.max_position_size))
        return final_pct

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
