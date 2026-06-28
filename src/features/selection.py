import numpy as np
import pandas as pd
from typing import List
from utils.logging_utils import setup_logger

logger = setup_logger("feature_selection")

def remove_highly_correlated_features(df: pd.DataFrame, feature_cols: List[str], threshold: float = 0.85) -> List[str]:
    """Identifies and removes highly correlated features to reduce redundancy.
    
    Keeps the first feature in a highly correlated pair and drops the second.
    """
    logger.info(f"Starting correlation-based feature selection (initial features: {len(feature_cols)})...")
    
    corr_matrix = df[feature_cols].corr().abs()
    
    # Select upper triangle of correlation matrix
    upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
    
    # Find features with correlation greater than threshold
    to_drop = [column for column in upper.columns if any(upper[column] > threshold)]
    
    selected_features = [col for col in feature_cols if col not in to_drop]
    
    logger.info(f"Feature selection complete. Dropped {len(to_drop)} features. Selected: {len(selected_features)}")
    return selected_features
