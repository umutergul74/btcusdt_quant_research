import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score
from typing import Any

def run_random_label_test(model: Any, X_train: np.ndarray, y_train: np.ndarray, X_val: np.ndarray, y_val: np.ndarray) -> float:
    """Trains the model on shuffled labels and evaluates accuracy on the validation set.
    
    The resulting accuracy should be close to random chance (0.5 for binary).
    """
    y_train_shuffled = y_train.copy()
    np.random.shuffle(y_train_shuffled)
    
    # Clone and fit
    import copy
    test_model = copy.deepcopy(model)
    test_model.fit(X_train, y_train_shuffled)
    
    preds = test_model.predict(X_val)
    acc = accuracy_score(y_val, preds)
    return acc

def run_shuffled_feature_test(model: Any, X_val: np.ndarray, y_val: np.ndarray) -> float:
    """Evaluates the model on validation data where features are shuffled.
    
    Performance should drop significantly.
    """
    X_val_shuffled = X_val.copy()
    for col_idx in range(X_val_shuffled.shape[1]):
        np.random.shuffle(X_val_shuffled[:, col_idx])
        
    preds = model.predict(X_val_shuffled)
    acc = accuracy_score(y_val, preds)
    return acc
