import numpy as np
from typing import List, Any, Optional

class CalibratedEnsemble:
    """Ensemble of multiple calibrated classifiers."""
    def __init__(self, models: List[Any], weights: Optional[List[float]] = None):
        self.models = models
        self.weights = weights or [1.0 / len(models)] * len(models)

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """Averages the predicted probabilities of the member models."""
        ensemble_probs = None
        for model, weight in zip(self.models, self.weights):
            probs = model.predict_proba(X)
            if ensemble_probs is None:
                ensemble_probs = probs * weight
            else:
                ensemble_probs += probs * weight
        return ensemble_probs

    def predict(self, X: np.ndarray, threshold: float = 0.5) -> np.ndarray:
        """Predicts binary class based on ensemble probability exceeding a threshold."""
        probs = self.predict_proba(X)
        # Assuming binary classification, class 1 is index 1
        return (probs[:, 1] >= threshold).astype(int)
