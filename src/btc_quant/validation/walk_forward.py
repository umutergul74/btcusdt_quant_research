import pandas as pd
from btc_quant.models.tabular import train_tabular_models
from btc_quant.validation.metrics import classification_summary
from btc_quant.validation.splits import walk_forward_splits

def run_walk_forward(X, y, model_config=None, min_folds=3, seed=42):
    rows = []
    for fold, (train_idx, val_idx) in enumerate(walk_forward_splits(len(X), min_folds=min_folds), start=1):
        models = train_tabular_models(X.iloc[train_idx], y.iloc[train_idx], enabled=(model_config or {}).get("models", {}), seed=seed)
        for model in models:
            pred = model.estimator.predict(X.iloc[val_idx])
            metrics = classification_summary(y.iloc[val_idx], pred)
            metrics.update({"fold": fold, "model": model.name, "train_rows": int(len(train_idx)), "validation_rows": int(len(val_idx))})
            rows.append(metrics)
    return pd.DataFrame(rows)

