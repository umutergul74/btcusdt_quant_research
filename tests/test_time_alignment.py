from btc_quant.data.downloader import create_synthetic_ohlcv
from btc_quant.features.registry import build_features
from btc_quant.labels.forward_returns import build_forward_return_labels

def test_feature_and_label_time_alignment():
    frame = create_synthetic_ohlcv(rows=80)
    features = build_features(frame)
    labels = build_forward_return_labels(frame, horizon_bars=6)
    assert (features["feature_available_time"] <= features["decision_time"]).all()
    assert (labels["label_end_time"] > labels["decision_time"]).all()

