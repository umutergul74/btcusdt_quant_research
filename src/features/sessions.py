import pandas as pd
import numpy as np

def compute_session_features(df: pd.DataFrame) -> pd.DataFrame:
    """Computes session-related features based on UTC time.
    
    Sessions (UTC):
    - Asia: 00:00 - 08:00
    - London: 08:00 - 16:00
    - New York: 13:00 - 21:00
    """
    res = df.copy()
    
    # Ensure index is datetime
    if not isinstance(res.index, pd.DatetimeIndex):
        raise ValueError("DataFrame index must be a DatetimeIndex.")
        
    hours = res.index.hour
    
    # Session flags
    res["session_asia"] = (hours >= 0) & (hours < 8)
    res["session_london"] = (hours >= 8) & (hours < 16)
    res["session_new_york"] = (hours >= 13) & (hours < 21)
    res["session_overlap"] = (hours >= 13) & (hours < 16) # London / NY overlap
    
    # Time indicators
    res["hour_of_day"] = hours
    res["day_of_week"] = res.index.dayofweek
    res["is_weekend"] = res.index.dayofweek >= 5
    
    # Session high/low trackers (24h rolling is a good proxy, or session-specific)
    # We can compute the high/low of the Asia session to use as a key level for London/NY
    # To keep it vectorised and fast, we can use rolling windows matching the session lengths.
    
    return res
