import numpy as np

def classification_summary(y_true, y_pred):
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    labels = [-1, 0, 1]
    accuracy = float((y_true == y_pred).mean()) if len(y_true) else 0.0
    f1s, recalls, precisions = [], [], []
    for label in labels:
        tp = ((y_true == label) & (y_pred == label)).sum()
        fp = ((y_true != label) & (y_pred == label)).sum()
        fn = ((y_true == label) & (y_pred != label)).sum()
        precision = tp / (tp + fp) if (tp + fp) else 0.0
        recall = tp / (tp + fn) if (tp + fn) else 0.0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0.0
        precisions.append(float(precision)); recalls.append(float(recall)); f1s.append(float(f1))
    return {"accuracy": accuracy, "balanced_accuracy": float(np.mean(recalls)), "macro_precision": float(np.mean(precisions)), "macro_recall": float(np.mean(recalls)), "macro_f1": float(np.mean(f1s))}

