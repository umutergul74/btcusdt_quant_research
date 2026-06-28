import numpy as np
import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score, precision_recall_curve, auc, brier_score_loss
from typing import Dict, Any

def calculate_advanced_ml_metrics(y_true: np.ndarray, y_prob: np.ndarray, threshold: float = 0.5) -> Dict[str, Any]:
    """Computes advanced financial ML validation metrics.
    
    - y_true: Ground truth binary labels (0 or 1)
    - y_prob: Predicted probability of the positive class (1)
    """
    # Binary predictions based on threshold
    y_pred = (y_prob >= threshold).astype(int)
    
    # Classification metrics
    precision = precision_score(y_true, y_pred, zero_division=0)
    recall = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)
    
    # Precision-Recall AUC (Crucial for imbalanced financial datasets)
    precisions, recalls, _ = precision_recall_curve(y_true, y_prob)
    pr_auc = auc(recalls, precisions)
    
    # Calibration metrics (Brier Score: lower is better)
    brier = brier_score_loss(y_true, y_prob)
    
    # Expected Calibration Error (ECE) approximation
    # Group predictions into bins and calculate the difference between confidence and accuracy
    n_bins = 10
    bin_boundaries = np.linspace(0, 1, n_bins + 1)
    ece = 0.0
    n_samples = len(y_true)
    
    for i in range(n_bins):
        bin_lower = bin_boundaries[i]
        bin_upper = bin_boundaries[i + 1]
        in_bin = (y_prob >= bin_lower) & (y_prob < bin_upper)
        prop_in_bin = np.mean(in_bin)
        
        if prop_in_bin > 0:
            accuracy_in_bin = np.mean(y_true[in_bin])
            avg_confidence_in_bin = np.mean(y_prob[in_bin])
            ece += prop_in_bin * np.abs(avg_confidence_in_bin - accuracy_in_bin)
            
    return {
        "precision": precision,
        "recall": recall,
        "f1_score": f1,
        "pr_auc": pr_auc,
        "brier_score": brier,
        "ece": ece
    }
