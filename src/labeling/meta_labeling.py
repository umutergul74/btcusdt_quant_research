import pandas as pd
import numpy as np

def generate_meta_labels(df_barriers: pd.DataFrame) -> pd.Series:
    """Generates meta-labels for a two-stage modeling approach.
    
    A meta-label of 1 indicates the trade hit the take-profit barrier (label == 1).
    A meta-label of 0 indicates the trade hit the stop-loss or timed out (label in [-1, 0]).
    """
    if "label" not in df_barriers.columns:
        raise ValueError("DataFrame must contain a 'label' column from the triple barrier method.")
        
    return (df_barriers["label"] == 1).astype(int)
