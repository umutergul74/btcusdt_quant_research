import pandas as pd
import numpy as np

def compute_confluence_score(df: pd.DataFrame) -> pd.DataFrame:
    """Computes rule-based confluence scores for bullish and bearish setups."""
    res = df.copy()
    
    # 1. Bullish Confluence Components
    # - In discount zone (score +1)
    # - Bullish sweep (score +2)
    # - Bullish CVD divergence (score +2)
    # - Bullish FVG created or mitigated (score +1)
    # - Bullish OB or Breaker reaction (score +1)
    
    bull_score = pd.Series(0.0, index=res.index)
    if "in_discount" in res:
        bull_score += np.where(res["in_discount"], 1.0, 0.0)
    if "bullish_sweep_24h" in res:
        bull_score += np.where(res["bullish_sweep_24h"], 2.0, 0.0)
    if "bullish_cvd_divergence" in res:
        bull_score += np.where(res["bullish_cvd_divergence"], 2.0, 0.0)
    if "bullish_fvg" in res:
        bull_score += np.where(res["bullish_fvg"], 1.0, 0.0)
    if "bullish_ob" in res:
        bull_score += np.where(res["bullish_ob"], 1.0, 0.0)
        
    # 2. Bearish Confluence Components
    # - In premium zone (score +1)
    # - Bearish sweep (score +2)
    # - Bearish CVD divergence (score +2)
    # - Bearish FVG created or mitigated (score +1)
    # - Bearish OB or Breaker reaction (score +1)
    
    bear_score = pd.Series(0.0, index=res.index)
    if "in_premium" in res:
        bear_score += np.where(res["in_premium"], 1.0, 0.0)
    if "bearish_sweep_24h" in res:
        bear_score += np.where(res["bearish_sweep_24h"], 2.0, 0.0)
    if "bearish_cvd_divergence" in res:
        bear_score += np.where(res["bearish_cvd_divergence"], 2.0, 0.0)
    if "bearish_fvg" in res:
        bear_score += np.where(res["bearish_fvg"], 1.0, 0.0)
    if "bearish_ob" in res:
        bear_score += np.where(res["bearish_ob"], 1.0, 0.0)
        
    res["confluence_bullish_score"] = bull_score
    res["confluence_bearish_score"] = bear_score
    
    # Final confluence score (positive = bullish, negative = bearish)
    res["confluence_score"] = bull_score - bear_score
    
    return res
