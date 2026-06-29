import numpy as np
import pandas as pd

def create_synthetic_ohlcv(rows=1500, freq="5min", seed=42, symbol="BTCUSDT"):
    rng = np.random.default_rng(seed)
    close_time = pd.date_range("2022-01-01", periods=rows, freq=freq, tz="UTC")
    open_time = close_time - pd.Timedelta(freq)
    returns = rng.normal(0.0, 0.0007, rows) + 0.00015 * np.sin(np.linspace(0, 20, rows))
    close = 42000 * np.exp(np.cumsum(returns))
    open_ = np.r_[close[0], close[:-1]]
    spread = close * np.abs(rng.normal(0.0008, 0.00025, rows))
    high = np.maximum(open_, close) + spread
    low = np.minimum(open_, close) - spread
    volume = rng.lognormal(6.0, 0.4, rows)
    taker_buy = volume * rng.uniform(0.42, 0.58, rows)
    quote_volume = volume * close
    return pd.DataFrame({
        "bar_open_time": open_time, "bar_close_time": close_time,
        "open": open_, "high": high, "low": low, "close": close,
        "volume": volume, "quote_volume": quote_volume,
        "number_of_trades": rng.integers(100, 2000, rows),
        "taker_buy_base_volume": taker_buy,
        "taker_buy_quote_volume": taker_buy * close,
        "taker_sell_base_volume": volume - taker_buy,
        "taker_sell_quote_volume": quote_volume - taker_buy * close,
        "source": "synthetic_debug", "symbol": symbol, "timeframe": "5m",
    })

