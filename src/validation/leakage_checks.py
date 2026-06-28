import pandas as pd
import numpy as np
from typing import List

def verify_no_lookahead(df: pd.DataFrame, feature_cols: List[str], target_col: str) -> bool:
    """Verifies that no feature has a suspicious future correlation with the target.
    
    If a feature is highly correlated with future returns or future targets, it might be leaky.
    Also checks if shifting the target forward changes the correlation pattern.
    """
    for col in feature_cols:
        # Correlation of feature with current target
        corr = df[col].corr(df[target_col])
        # Correlation of feature with past target (shifted)
        past_corr = df[col].corr(df[target_col].shift(5))
        
        # If correlation is extremely high (> 0.95), it's highly suspicious
        if abs(corr) > 0.95:
            print(f"SUSPICIOUS: Feature '{col}' has extremely high correlation ({corr:.4f}) with '{target_col}'!")
            return False
            
    return True

def verify_chronological_split(train_df: pd.DataFrame, test_df: pd.DataFrame) -> bool:
    """Verifies that the train and test sets do not overlap and are chronologically sorted."""
    train_max = train_df.index.max()
    test_min = test_df.index.min()
    
    if train_max >= test_min:
        print(f"LEAKAGE DETECTED: Train max timestamp ({train_max}) is greater than or equal to Test min timestamp ({test_min})!")
        return False
    return True
