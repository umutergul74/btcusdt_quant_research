from btc_quant.data.contracts import REQUIRED_OHLCV_COLUMNS
from btc_quant.data.downloader import create_synthetic_ohlcv
from btc_quant.data.quality import validate_ohlcv

def test_synthetic_ohlcv_contract_passes():
    frame = create_synthetic_ohlcv(rows=100)
    assert all(col in frame.columns for col in REQUIRED_OHLCV_COLUMNS)
    assert validate_ohlcv(frame)["status"] == "PASS"

