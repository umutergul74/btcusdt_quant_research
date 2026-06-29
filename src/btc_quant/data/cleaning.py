import pandas as pd

def clean_ohlcv(frame):
    out = frame.copy()
    out["bar_open_time"] = pd.to_datetime(out["bar_open_time"], utc=True)
    out["bar_close_time"] = pd.to_datetime(out["bar_close_time"], utc=True)
    out = out.sort_values(["symbol", "timeframe", "bar_close_time"])
    out = out.drop_duplicates(["symbol", "timeframe", "bar_close_time"], keep="last")
    valid = (out["high"] >= out[["open", "close"]].max(axis=1)) & (out["low"] <= out[["open", "close"]].min(axis=1))
    return out[valid].reset_index(drop=True)

