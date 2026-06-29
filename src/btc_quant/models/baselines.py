import numpy as np
import pandas as pd
from btc_quant.validation.metrics import classification_summary

def baseline_predictions(y_true, seed=42):
    rng = np.random.default_rng(seed)
    values = np.array([-1, 0, 1])
    probs = y_true.value_counts(normalize=True).reindex(values, fill_value=0.0).to_numpy()
    probs = probs / probs.sum() if probs.sum() else np.array([1/3, 1/3, 1/3])
    return {
        "always_long": np.ones(len(y_true), dtype=int),
        "always_short": -np.ones(len(y_true), dtype=int),
        "always_no_trade": np.zeros(len(y_true), dtype=int),
        "rate_matched_random": rng.choice(values, size=len(y_true), p=probs),
    }

def evaluate_baselines(y_true, seed=42):
    rows = []
    for name, pred in baseline_predictions(y_true, seed).items():
        metrics = classification_summary(y_true, pred)
        metrics["model"] = name
        rows.append(metrics)
    return pd.DataFrame(rows).sort_values("macro_f1", ascending=False)

