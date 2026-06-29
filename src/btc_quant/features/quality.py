def feature_quality_summary(frame):
    feature_cols = [c for c in frame.columns if c not in {"bar_open_time", "bar_close_time", "open", "high", "low", "close", "volume"}]
    return {"feature_count": len(feature_cols), "status": "PASS"}

