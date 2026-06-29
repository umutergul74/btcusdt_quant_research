def evaluate_phase1_gate(checks):
    required_failures = [name for name, passed in checks.items() if passed is False]
    status = "RED" if required_failures else "YELLOW"
    return {"gate_status": status, "phase2_allowed": False, "promotion_allowed": False, "required_failures": required_failures, "decision": "DO_NOT_PROCEED_TO_PHASE2", "canonical_next_action": "continue_phase1_model_improvement"}

