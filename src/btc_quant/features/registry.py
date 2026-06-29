import pandas as pd

def build_features(frame):
    df = frame.sort_values("bar_close_time").copy()
    close = df["close"]
    high = df["high"]
    low = df["low"]
    rng = (high - low).replace(0, pd.NA)
    df["ret_1"] = close.pct_change()
    df["ret_3"] = close.pct_change(3)
    df["rolling_high_20"] = high.rolling(20, min_periods=5).max()
    df["rolling_low_20"] = low.rolling(20, min_periods=5).min()
    df["range_position_20"] = (close - df["rolling_low_20"]) / (df["rolling_high_20"] - df["rolling_low_20"]).replace(0, pd.NA)
    df["swing_high_confirmed_3"] = (high.shift(3) == high.shift(1).rolling(5, min_periods=5).max()).astype(float)
    df["swing_low_confirmed_3"] = (low.shift(3) == low.shift(1).rolling(5, min_periods=5).min()).astype(float)
    df["body_to_range"] = (df["close"] - df["open"]).abs() / rng
    df["bullish_fvg"] = (low > high.shift(2)).astype(int)
    df["bearish_fvg"] = (high < low.shift(2)).astype(int)
    prev_high = high.shift(1).rolling(20, min_periods=5).max()
    prev_low = low.shift(1).rolling(20, min_periods=5).min()
    df["swept_prior_20_high"] = (high > prev_high).astype(int)
    df["swept_prior_20_low"] = (low < prev_low).astype(int)
    sell = df.get("taker_sell_base_volume", df["volume"] - df["taker_buy_base_volume"])
    df["taker_buy_ratio"] = df["taker_buy_base_volume"] / df["volume"].replace(0, pd.NA)
    df["volume_delta_proxy"] = df["taker_buy_base_volume"] - sell
    df["cvd_proxy_48"] = df["volume_delta_proxy"].rolling(48, min_periods=12).sum()
    tr = pd.concat([(high-low).abs(), (high-close.shift(1)).abs(), (low-close.shift(1)).abs()], axis=1).max(axis=1)
    df["atr_14"] = tr.rolling(14, min_periods=5).mean()
    df["realized_vol_48"] = close.pct_change().rolling(48, min_periods=12).std()
    hour = pd.to_datetime(df["bar_close_time"], utc=True).dt.hour
    df["hour_utc"] = hour
    df["session_asia"] = ((hour >= 0) & (hour < 8)).astype(int)
    df["session_london"] = ((hour >= 7) & (hour < 16)).astype(int)
    df["session_new_york"] = ((hour >= 13) & (hour < 22)).astype(int)
    df["ema_20"] = close.ewm(span=20, adjust=False).mean()
    df["ema_50"] = close.ewm(span=50, adjust=False).mean()
    df["ema_20_50_spread"] = df["ema_20"] / df["ema_50"] - 1
    df["feature_available_time"] = pd.to_datetime(df["bar_close_time"], utc=True)
    df["decision_time"] = df["feature_available_time"]
    return df

