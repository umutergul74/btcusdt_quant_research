import lightgbm as lgb
import xgboost as xgb
from catboost import CatBoostClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from typing import Any, Dict, Optional
import numpy as np

class TabularModelWrapper:
    """Wrapper for tabular machine learning classifiers."""
    def __init__(self, model_type: str = "lightgbm", params: Optional[Dict[str, Any]] = None):
        self.model_type = model_type
        self.params = params or {}
        self.model = self._init_model()

    def _init_model(self) -> Any:
        if self.model_type == "lightgbm":
            return lgb.LGBMClassifier(**self.params)
        elif self.model_type == "xgboost":
            return xgb.XGBClassifier(**self.params)
        elif self.model_type == "catboost":
            # Set verbose=0 to avoid cluttering logs
            if "verbose" not in self.params:
                self.params["verbose"] = 0
            return CatBoostClassifier(**self.params)
        elif self.model_type == "random_forest":
            return RandomForestClassifier(**self.params)
        elif self.model_type == "logistic_regression":
            return LogisticRegression(**self.params)
        else:
            raise ValueError(f"Unknown model type: {self.model_type}")

    def fit(self, X: np.ndarray, y: np.ndarray):
        """Fits the model on the training data."""
        self.model.fit(X, y)

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predicts classes."""
        return self.model.predict(X)

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """Predicts class probabilities."""
        return self.model.predict_proba(X)

    def get_feature_importance(self) -> Optional[np.ndarray]:
        """Retrieves feature importances if available."""
        if hasattr(self.model, "feature_importances_"):
            return self.model.feature_importances_
        elif hasattr(self.model, "coef_"):
            return self.model.coef_[0]
        return None
