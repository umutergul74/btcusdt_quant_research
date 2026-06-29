from btc_quant.data.downloader import create_synthetic_ohlcv
from btc_quant.labels.forward_returns import build_forward_return_labels

def test_labels_do_not_exceed_source_rows():
    labels = build_forward_return_labels(create_synthetic_ohlcv(rows=50), horizon_bars=10)
    assert len(labels) < 50
    assert {"decision_time", "label_start_time", "label_end_time", "target"}.issubset(labels.columns)

