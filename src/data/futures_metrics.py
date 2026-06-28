import time
import requests
import pandas as pd
from typing import Optional, List, Dict, Any
from utils.logging_utils import setup_logger

logger = setup_logger("futures_metrics")

class FuturesMetricsDownloader:
    """Downloader for Binance Futures-specific metrics (funding rates, open interest, long/short ratios)."""
    def __init__(self):
        self.base_url = "https://fapi.binance.com"

    def download_funding_rates(
        self, 
        symbol: str, 
        start_time_ms: int, 
        end_time_ms: Optional[int] = None
    ) -> pd.DataFrame:
        """Downloads historical funding rates for a symbol."""
        url = f"{self.base_url}/fapi/v1/fundingRate"
        params = {
            "symbol": symbol,
            "startTime": start_time_ms,
            "limit": 1000
        }
        if end_time_ms:
            params["endTime"] = end_time_ms

        logger.info(f"Downloading funding rates for {symbol}...")
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if not data:
                return pd.DataFrame()

            df = pd.DataFrame(data)
            df = df.rename(columns={"fundingTime": "timestamp", "fundingRate": "funding_rate"})
            df["timestamp"] = df["timestamp"].astype(int)
            df["funding_rate"] = df["funding_rate"].astype(float)
            df = df[["timestamp", "funding_rate"]]
            return df
        except Exception as e:
            logger.error(f"Failed to download funding rates: {e}")
            return pd.DataFrame()

    def download_open_interest(
        self, 
        symbol: str, 
        timeframe: str, 
        start_time_ms: int, 
        end_time_ms: Optional[int] = None
    ) -> pd.DataFrame:
        """Downloads historical open interest for a symbol."""
        # Binance Futures Data API
        url = "https://fapi.binance.com/futures/data/openInterestHist"
        params = {
            "symbol": symbol,
            "period": timeframe,  # e.g. "5m", "15m", "1h", "4h", "1d"
            "startTime": start_time_ms,
            "limit": 500
        }
        if end_time_ms:
            params["endTime"] = end_time_ms

        logger.info(f"Downloading open interest history for {symbol} ({timeframe})...")
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if not data or not isinstance(data, list):
                return pd.DataFrame()

            df = pd.DataFrame(data)
            df = df.rename(columns={"timestamp": "timestamp", "sumOpenInterest": "open_interest", "sumOpenInterestValue": "open_interest_value"})
            df["timestamp"] = df["timestamp"].astype(int)
            df["open_interest"] = df["open_interest"].astype(float)
            df["open_interest_value"] = df["open_interest_value"].astype(float)
            df = df[["timestamp", "open_interest", "open_interest_value"]]
            return df
        except Exception as e:
            logger.error(f"Failed to download open interest: {e}")
            return pd.DataFrame()
