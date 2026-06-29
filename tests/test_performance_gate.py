from btc_quant.validation.gate import evaluate_phase1_gate

def test_gate_never_allows_phase2_in_phase1():
    result = evaluate_phase1_gate({"data_quality": True, "label_quality": True, "no_leakage": True})
    assert result["phase2_allowed"] is False
    assert result["decision"] == "DO_NOT_PROCEED_TO_PHASE2"

