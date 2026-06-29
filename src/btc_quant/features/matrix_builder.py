IDENTIFIER_COLUMNS = {"bar_open_time", "bar_close_time", "feature_available_time", "decision_time", "label_start_time", "label_end_time", "source", "symbol", "timeframe", "target", "forward_return", "label_type"}

def feature_columns(frame):
    return [c for c in frame.select_dtypes(include="number").columns if c not in IDENTIFIER_COLUMNS and not c.startswith("label_")]

def build_xy(frame):
    cols = feature_columns(frame)
    data = frame.dropna(subset=cols + ["target"]).copy()
    return data[cols], data["target"].astype(int), cols, data

