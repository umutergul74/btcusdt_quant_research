import pandas as pd
from btc_quant.core.exceptions import LeakageCheckError

FORBIDDEN_FEATURE_TOKENS = ("label", "target", "forward_return", "future_")

def check_feature_availability(frame, raise_on_error=False):
    errors = []
    if "feature_available_time" not in frame.columns or "decision_time" not in frame.columns:
        errors.append("missing_feature_available_time_or_decision_time")
    else:
        if (pd.to_datetime(frame["feature_available_time"], utc=True) > pd.to_datetime(frame["decision_time"], utc=True)).any():
            errors.append("feature_available_time_after_decision_time")
    numeric_cols = frame.select_dtypes(include="number").columns
    forbidden = [c for c in numeric_cols if any(token in c.lower() for token in FORBIDDEN_FEATURE_TOKENS)]
    if forbidden:
        errors.append("forbidden_feature_columns:" + ",".join(forbidden))
    if errors and raise_on_error:
        raise LeakageCheckError("; ".join(errors))
    return {"status": "PASS" if not errors else "FAIL", "errors": errors}

