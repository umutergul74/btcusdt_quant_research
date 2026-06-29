from btc_quant.core.exceptions import Phase2BlockedError

def phase2_blocked():
    raise Phase2BlockedError("Phase 2 is blocked until Future-OOS promotion rules pass.")

