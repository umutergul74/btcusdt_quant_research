import pandas as pd
from btc_quant.validation.leakage import check_feature_availability

def test_leakage_check_blocks_label_feature():
    frame = pd.DataFrame({"feature_available_time": ["2022-01-01T00:00:00Z"], "decision_time": ["2022-01-01T00:00:00Z"], "future_return_feature": [1.0]})
    assert check_feature_availability(frame)["status"] == "FAIL"

