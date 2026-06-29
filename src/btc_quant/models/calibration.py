import numpy as np

def brier_score_binary(y_true, prob_positive):
    y = np.asarray(y_true) == 1
    p = np.asarray(prob_positive, dtype=float)
    return float(np.mean((p - y.astype(float)) ** 2)) if len(p) else float("nan")

def expected_calibration_error(y_true, prob_positive, bins=10):
    y = (np.asarray(y_true) == 1).astype(float)
    p = np.asarray(prob_positive, dtype=float)
    if len(p) == 0:
        return float("nan")
    edges = np.linspace(0, 1, bins + 1)
    ece = 0.0
    for lo, hi in zip(edges[:-1], edges[1:]):
        mask = (p >= lo) & (p < hi if hi < 1 else p <= hi)
        if mask.any():
            ece += mask.mean() * abs(p[mask].mean() - y[mask].mean())
    return float(ece)

