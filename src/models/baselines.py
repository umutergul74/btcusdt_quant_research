import numpy as np
import pandas as pd
from typing import Union

class BaselineModel:
    """Base class for baseline trading models."""
    def __init__(self, strategy: str = "always_long"):
        self.strategy = strategy

    def predict(self, df: pd.DataFrame) -> np.ndarray:
        """Predicts the trade direction (+1, -1, 0) for each row."""
        n_samples = len(df)
        if self.strategy == "always_long":
            return np.ones(n_samples)
        elif self.strategy == "always_short":
            return -np.ones(n_samples)
        elif self.strategy == "random":
            return np.random.choice([1, -1, 0], size=n_samples, p=[0.4, 0.4, 0.2])
        elif self.strategy == "trend_following":
            # Simple trend following: +1 if price > 20 EMA, else -1
            ema20 = df["close"].ewm(span=20).mean()
            return np.where(df["close"] > ema20, 1, -1)
        elif self.strategy == "mean_reversion":
            # Simple mean reversion: +1 if price < lower Bollinger Band, -1 if price > upper BB
            rolling_mean = df["close"].rolling(20).mean()
            rolling_std = df["close"].rolling(20).std()
            lower_bb = rolling_mean - 2 * rolling_std
            upper_bb = rolling_mean + 2 * rolling_std
            return np.where(df["close"] < lower_bb, 1, np.where(df["close"] > upper_bb, -1, 0))
        else:
            raise ValueError(f"Unknown baseline strategy: {self.strategy}")
            
    def predict_proba(self, df: pd.DataFrame) -> np.ndarray:
        """Predicts probabilities [prob_short, prob_no_trade, prob_long]."""
        n_samples = len(df)
        preds = self.predict(df)
        
        # Convert predictions to one-hot probability arrays
        probas = np.zeros((n_samples, 3))
        for idx, pred in enumerate(preds):
            if pred == -1:
                probas[idx, 0] = 1.0
            elif pred == 0:
                probas[idx, 1] = 1.0
            elif pred == 1:
                probas[idx, 2] = 1.0
        return probas
