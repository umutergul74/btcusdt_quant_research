from sklearn.calibration import CalibratedClassifierCV
from sklearn.isotonic import IsotonicRegression
import numpy as np
from typing import Any

class ProbabilityCalibrator:
    """Calibrates model output probabilities using Platt Scaling or Isotonic Regression."""
    def __init__(self, method: str = "isotonic"):
        self.method = method
        self.calibrator = None

    def fit(self, probs: np.ndarray, y: np.ndarray):
        """Fits the calibrator on predicted probabilities and true labels.
        
        y must be binary (0 or 1).
        """
        # Ensure probs is a 1D array of the positive class probabilities
        if probs.ndim > 1:
            probs = probs[:, 1]
            
        if self.method == "isotonic":
            self.calibrator = IsotonicRegression(out_of_bounds="clip")
            self.calibrator.fit(probs, y)
        elif self.method == "platt":
            # Platt scaling is equivalent to logistic regression on the probabilities
            from sklearn.linear_model import LogisticRegression
            self.calibrator = LogisticRegression(C=1e5)
            self.calibrator.fit(probs.reshape(-1, 1), y)
        else:
            raise ValueError(f"Unknown calibration method: {self.method}")

    def calibrate(self, probs: np.ndarray) -> np.ndarray:
        """Applies calibration to raw probabilities."""
        if self.calibrator is None:
            raise ValueError("Calibrator has not been fitted yet.")
            
        if probs.ndim > 1:
            pos_probs = probs[:, 1]
        else:
            pos_probs = probs
            
        if self.method == "isotonic":
            calibrated_pos = self.calibrator.predict(pos_probs)
        elif self.method == "platt":
            calibrated_pos = self.calibrator.predict_proba(pos_probs.reshape(-1, 1))[:, 1]
            
        # Reconstruct 2D probability array [class_0, class_1]
        calibrated_probs = np.zeros((len(pos_probs), 2))
        calibrated_probs[:, 1] = calibrated_pos
        calibrated_probs[:, 0] = 1.0 - calibrated_pos
        return calibrated_probs
