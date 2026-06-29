from btc_quant.data.contracts import REQUIRED_OHLCV_COLUMNS

def validate_ohlcv(frame):
    missing = [c for c in REQUIRED_OHLCV_COLUMNS if c not in frame.columns]
    result = {"rows": int(len(frame)), "missing_columns": missing, "status": "PASS"}
    if missing:
        result["status"] = "FAIL"
        return result
    result["duplicate_bar_close_time_rows"] = int(frame.duplicated(["symbol", "timeframe", "bar_close_time"]).sum())
    result["invalid_ohlc_rows"] = int(((frame["high"] < frame[["open", "close"]].max(axis=1)) | (frame["low"] > frame[["open", "close"]].min(axis=1))).sum())
    result["zero_volume_rows"] = int((frame["volume"] <= 0).sum())
    if result["duplicate_bar_close_time_rows"] or result["invalid_ohlc_rows"] or result["zero_volume_rows"]:
        result["status"] = "FAIL"
    return result

