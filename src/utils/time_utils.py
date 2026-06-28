import pandas as pd
from typing import Union

def convert_to_utc(df: pd.DataFrame, timestamp_col: str) -> pd.DataFrame:
    """Converts a timestamp column in a DataFrame to UTC datetime format and sets it as index."""
    df = df.copy()
    df[timestamp_col] = pd.to_datetime(df[timestamp_col], unit="ms", utc=True)
    df = df.sort_values(by=timestamp_col)
    df = df.set_index(timestamp_col)
    return df

def timestamp_to_ms(ts: Union[str, pd.Timestamp]) -> int:
    """Converts a string or Timestamp to millisecond epoch."""
    return int(pd.to_datetime(ts).value // 10**6)
