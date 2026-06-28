import pandas as pd
from typing import List

def resample_ohlcv(df: pd.DataFrame, rule: str) -> pd.DataFrame:
    """Resamples OHLCV data to a higher timeframe.
    
    df must have a datetime index.
    """
    resampler = df.resample(rule)
    resampled = pd.DataFrame({
        "open": resampler["open"].first(),
        "high": resampler["high"].max(),
        "low": resampler["low"].min(),
        "close": resampler["close"].last(),
        "volume": resampler["volume"].sum()
    })
    return resampled.dropna()

def align_htf_to_ltf(
    ltf_df: pd.DataFrame, 
    htf_df: pd.DataFrame, 
    htf_columns: List[str], 
    suffix: str
) -> pd.DataFrame:
    """Aligns higher timeframe (HTF) features to lower timeframe (LTF) safely.
    
    To prevent look-ahead bias:
    1. An HTF candle is only complete at the end of its period.
    2. We shift the HTF features by 1 candle (or align them using the closed timestamp).
    3. We forward-fill the shifted HTF features onto the LTF timeline.
    
    Both DataFrames must have datetime index in UTC.
    """
    ltf = ltf_df.copy()
    htf = htf_df[htf_columns].copy()
    
    # Rename HTF columns to avoid collision
    htf.columns = [f"{col}_{suffix}" for col in htf.columns]
    
    # Shift HTF features by 1 candle so that the features of the candle closing at T
    # are only available at and after T (i.e. we don't know the close of the 1h candle
    # starting at 09:00 until 10:00).
    # Since the index of htf_df represents the START of the candle, shifting it forward
    # by 1 HTF index makes it available only after that candle completes.
    # Alternatively, if the index represents the start, the candle completes at index + duration.
    # If we shift(1), the value at index T (start of candle) becomes the value of the candle
    # that started at T-1 and closed at T. This is exactly what we want!
    htf_shifted = htf.shift(1)
    
    # Reindex/join with LTF using forward fill
    aligned = ltf.join(htf_shifted, how="left")
    aligned[htf_shifted.columns] = aligned[htf_shifted.columns].ffill()
    
    return aligned
