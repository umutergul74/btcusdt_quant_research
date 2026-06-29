from datetime import datetime, timezone
import pandas as pd

def utc_now_iso():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

def ensure_utc(series):
    return pd.to_datetime(series, utc=True)

