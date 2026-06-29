from btc_quant.validation.metrics import classification_summary

def test_classification_summary_bounds():
    result = classification_summary([1, 0, -1], [1, 1, -1])
    assert 0 <= result["accuracy"] <= 1
    assert 0 <= result["macro_f1"] <= 1

