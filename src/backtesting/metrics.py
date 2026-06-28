import numpy as np
import pandas as pd
from typing import Dict, Any

def compute_performance_metrics(returns: pd.Series, equity: pd.Series) -> Dict[str, Any]:
    """Computes trading performance metrics from trade returns and equity curve."""
    if returns.empty:
        return {}
        
    win_trades = returns[returns > 0]
    loss_trades = returns[returns <= 0]
    
    win_rate = len(win_trades) / len(returns) if len(returns) > 0 else 0.0
    avg_win = win_trades.mean() if not win_trades.empty else 0.0
    avg_loss = loss_trades.mean() if not loss_trades.empty else 0.0
    payoff_ratio = abs(avg_win / avg_loss) if avg_loss != 0 else 0.0
    
    # Calculate drawdown
    running_max = equity.cummax()
    drawdowns = (equity - running_max) / running_max
    max_dd = drawdowns.min()
    
    # Sharpe & Sortino (assuming daily-like frequency of trades)
    avg_return = returns.mean()
    std_return = returns.std()
    downside_std = returns[returns < 0].std()
    
    sharpe = (avg_return / std_return * np.sqrt(252)) if std_return > 0 else 0.0
    sortino = (avg_return / downside_std * np.sqrt(252)) if downside_std > 0 else 0.0
    
    profit_factor = win_trades.sum() / abs(loss_trades.sum()) if not loss_trades.empty and loss_trades.sum() != 0 else 0.0
    expectancy = (win_rate * avg_win) + ((1 - win_rate) * avg_loss)
    
    return {
        "total_trades": len(returns),
        "win_rate": win_rate,
        "avg_win": avg_win,
        "avg_loss": avg_loss,
        "payoff_ratio": payoff_ratio,
        "max_drawdown": max_dd,
        "sharpe_ratio": sharpe,
        "sortino_ratio": sortino,
        "profit_factor": profit_factor,
        "expectancy": expectancy
    }
