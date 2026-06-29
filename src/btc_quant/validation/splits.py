import numpy as np

def chronological_train_test_split(n_rows, test_fraction=0.2):
    split = max(1, int(n_rows * (1 - test_fraction)))
    return np.arange(0, split), np.arange(split, n_rows)

def walk_forward_splits(n_rows, min_folds=3, train_fraction_initial=0.5, validation_fraction=0.15, embargo_bars=0):
    train_end = int(n_rows * train_fraction_initial)
    val_size = max(1, int(n_rows * validation_fraction))
    folds = []
    start = train_end
    while start + embargo_bars + val_size <= n_rows and len(folds) < max(min_folds, 1):
        train_idx = np.arange(0, start)
        val_idx = np.arange(start + embargo_bars, start + embargo_bars + val_size)
        folds.append((train_idx, val_idx))
        start += val_size
    return folds

