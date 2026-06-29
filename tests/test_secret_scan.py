from btc_quant.github.secret_scan import scan_text

def test_secret_scan_detects_assignment():
    sample = "api_" + "key = " + "'abc123'"
    assert scan_text(sample)

