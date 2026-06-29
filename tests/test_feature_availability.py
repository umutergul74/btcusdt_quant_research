from btc_quant.data.downloader import create_synthetic_ohlcv
from btc_quant.features.registry import build_features
from btc_quant.validation.leakage import check_feature_availability

def test_feature_availability_check_passes():
    assert check_feature_availability(build_features(create_synthetic_ohlcv(rows=120)))["status"] == "PASS"

