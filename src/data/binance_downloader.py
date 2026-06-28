import time
import ccxt
import pandas as pd
from typing import Optional, List, Dict, Any
from utils.logging_utils import setup_logger

logger = setup_logger("binance_downloader")

class BinanceDownloader:
    """Incremental downloader for Binance OHLCV and market data."""
    def __init__(self, market_type: str = "swap"):
        self.market_type = market_type
        # Use CCXT for unified access
        self.exchange = ccxt.binance({
            'enableRateLimit': True,
            'options': {
                'defaultType': 'future' if market_type == 'swap' else 'spot'
            }
        })

    def download_ohlcv(
        self, 
        symbol: str, 
        timeframe: str, 
        start_time_ms: int, 
        end_time_ms: Optional[int] = None,
        limit: int = 1000
    ) -> pd.DataFrame:
        """Downloads historical OHLCV candles from a starting timestamp in milliseconds."""
        all_candles = []
        current_start = start_time_ms
        end_time_ms = end_time_ms or int(time.time() * 1000)

        logger.info(f"Starting download for {symbol} {timeframe} from {pd.to_datetime(current_start, unit='ms')}...")

        while current_start < end_time_ms:
            retries = 5
            backoff = 1.0
            candles = None
            
            while retries > 0:
                try:
                    candles = self.exchange.fetch_ohlcv(
                        symbol=symbol,
                        timeframe=timeframe,
                        since=current_start,
                        limit=limit
                    )
                    break
                except ccxt.RateLimitExceeded as e:
                    logger.warning(f"Rate limit exceeded: {e}. Retrying in {backoff}s...")
                    time.sleep(backoff)
                    backoff *= 2
                    retries -= 1
                except Exception as e:
                    logger.error(f"Error fetching OHLCV: {e}. Retrying in {backoff}s...")
                    time.sleep(backoff)
                    backoff *= 2
                    retries -= 1
            
            if not candles:
                logger.error(f"Failed to download candles after multiple retries.")
                break
                
            all_candles.extend(candles)
            
            # If we received fewer candles than the limit, we have reached the end of available data
            if len(candles) < limit:
                break
                
            # Move start time forward to the timestamp of the last candle + 1 ms (or timeframe equivalent)
            last_timestamp = candles[-1][0]
            if last_timestamp == current_start:
                # Prevent infinite loop if exchange returns same data
                break
            current_start = last_timestamp + 1
            time.sleep(self.exchange.rateLimit / 1000.0)

        if not all_candles:
            return pd.DataFrame()

        df = pd.DataFrame(
            all_candles,
            columns=["timestamp", "open", "high", "low", "close", "volume"]
        )
        # Drop duplicates
        df = df.drop_duplicates(subset=["timestamp"])
        return df
