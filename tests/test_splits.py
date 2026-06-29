from btc_quant.validation.splits import walk_forward_splits

def test_walk_forward_splits_are_chronological():
    for train_idx, val_idx in walk_forward_splits(100, min_folds=3, embargo_bars=2):
        assert train_idx.max() < val_idx.min()

