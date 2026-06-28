from typing import Dict, Any

def generate_trade_explanation(trade_data: Dict[str, Any]) -> str:
    """Generates a human-readable explanation card for a specific trade decision.
    
    Expected keys in trade_data:
        - decision: "LONG" or "SHORT"
        - confidence: float (0.0 to 1.0)
        - setup: str
        - htf_bias: str
        - entry: float
        - stop: float
        - tp1: float
        - tp2: float
        - rr: float
        - ev: str ("Positive", "Negative")
        - reasons: list of str
    """
    reasons_str = "\n".join([f"- {r}" for r in trade_data.get("reasons", [])])
    
    card = f"""
Decision: {trade_data.get('decision', 'NO-TRADE')}
Confidence: {trade_data.get('confidence', 0.0):.2f}
Setup: {trade_data.get('setup', 'N/A')}
HTF Bias: {trade_data.get('htf_bias', 'Neutral')}
Entry: {trade_data.get('entry', 0.0):.2f}
Stop: {trade_data.get('stop', 0.0):.2f}
TP1: {trade_data.get('tp1', 0.0):.2f}
TP2: {trade_data.get('tp2', 0.0):.2f}
Risk/Reward: {trade_data.get('rr', 0.0):.1f}
Expected Value After Costs: {trade_data.get('ev', 'N/A')}

Reasoning:
{reasons_str}
"""
    return card
