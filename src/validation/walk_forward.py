import pandas as pd
from typing import List, Tuple

def get_walk_forward_splits(
    df: pd.DataFrame, 
    train_size: int, 
    test_size: int, 
    embargo: int = 0
) -> List[Tuple[pd.DataFrame, pd.DataFrame]]:
    """Generates walk-forward chronological splits.
    
    Each split returns (train_df, test_df).
    - train_size: number of rows in the training set
    - test_size: number of rows in the testing set
    - embargo: number of rows to discard at the beginning of the test set to prevent leakage
    """
    splits = []
    n_samples = len(df)
    
    start_idx = 0
    while start_idx + train_size + test_size <= n_samples:
        train_end = start_idx + train_size
        test_start = train_end + embargo
        test_end = train_end + test_size
        
        if test_start >= n_samples:
            break
            
        train_df = df.iloc[start_idx:train_end]
        test_df = df.iloc[test_start:min(test_end, n_samples)]
        
        splits.append((train_df, test_df))
        # Slide window by test_size
        start_idx += test_size
        
    return splits
