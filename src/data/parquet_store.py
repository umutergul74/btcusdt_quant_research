import os
import pandas as pd
from typing import Optional
from utils.logging_utils import setup_logger
from utils.io_utils import save_parquet, load_parquet

logger = setup_logger("parquet_store")

class ParquetStore:
    """Manager for saving and loading datasets from the Parquet store on Google Drive."""
    def __init__(self, project_root: str = "/content/drive/MyDrive/btcusdt_quant_research"):
        self.project_root = project_root
        self.raw_dir = os.path.join(project_root, "data", "raw")
        self.processed_dir = os.path.join(project_root, "data", "processed")
        
        # Fallback to local paths if needed
        if not os.path.exists(os.path.join(project_root, "data")):
            self.raw_dir = os.path.join(os.getcwd(), "data", "raw")
            self.processed_dir = os.path.join(os.getcwd(), "data", "processed")

    def save_raw_klines(self, df: pd.DataFrame, symbol: str, timeframe: str) -> bool:
        """Saves raw klines to a Parquet file."""
        filename = f"{symbol}_{timeframe}_raw.parquet"
        path = os.path.join(self.raw_dir, "klines", filename)
        return save_parquet(df, path, logger)

    def load_raw_klines(self, symbol: str, timeframe: str) -> Optional[pd.DataFrame]:
        """Loads raw klines from a Parquet file."""
        filename = f"{symbol}_{timeframe}_raw.parquet"
        path = os.path.join(self.raw_dir, "klines", filename)
        return load_parquet(path, logger)

    def save_processed_klines(self, df: pd.DataFrame, symbol: str, timeframe: str) -> bool:
        """Saves processed/cleaned klines to a Parquet file."""
        filename = f"{symbol}_{timeframe}_clean.parquet"
        path = os.path.join(self.processed_dir, filename)
        return save_parquet(df, path, logger)

    def load_processed_klines(self, symbol: str, timeframe: str) -> Optional[pd.DataFrame]:
        """Loads processed/cleaned klines from a Parquet file."""
        filename = f"{symbol}_{timeframe}_clean.parquet"
        path = os.path.join(self.processed_dir, filename)
        return load_parquet(path, logger)
