import pandas as pd

def build_forward_return_labels(frame, horizon_bars=12, no_trade_threshold=0.0005, edge_threshold=0.0015):
    df = frame.sort_values("bar_close_time").copy()
    future_close = df["close"].shift(-horizon_bars)
    forward_return = future_close / df["close"] - 1.0
    target = pd.Series(0, index=df.index)
    target = target.mask(forward_return >= edge_threshold, 1)
    target = target.mask(forward_return <= -edge_threshold, -1)
    out = pd.DataFrame({
        "bar_close_time": pd.to_datetime(df["bar_close_time"], utc=True),
        "decision_time": pd.to_datetime(df["bar_close_time"], utc=True),
        "label_start_time": pd.to_datetime(df["bar_close_time"].shift(-1), utc=True),
        "label_end_time": pd.to_datetime(df["bar_close_time"].shift(-horizon_bars), utc=True),
        "forward_return": forward_return,
        "target": target,
        "label_type": "forward_return_threshold",
    })
    return out.dropna(subset=["label_start_time", "label_end_time", "forward_return"]).reset_index(drop=True)

