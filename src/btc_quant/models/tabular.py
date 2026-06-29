from dataclasses import dataclass
import numpy as np
try:
    from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier, ExtraTreesClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler
    SKLEARN_AVAILABLE = True
except Exception:
    SKLEARN_AVAILABLE = False

@dataclass
class TrainedModel:
    name: str
    estimator: object
    feature_columns: list

class MajorityClassModel:
    def fit(self, X, y):
        values, counts = np.unique(y, return_counts=True)
        self.majority_ = values[counts.argmax()] if len(values) else 0
        return self
    def predict(self, X):
        return np.full(len(X), self.majority_, dtype=int)

def train_tabular_models(X_train, y_train, enabled=None, seed=42):
    enabled = enabled or {}
    cols = list(X_train.columns)
    if not SKLEARN_AVAILABLE:
        return [TrainedModel("majority_fallback", MajorityClassModel().fit(X_train, y_train), cols)]
    candidates = []
    if enabled.get("logistic_regression", True):
        candidates.append(("logistic_regression", make_pipeline(StandardScaler(), LogisticRegression(max_iter=500, class_weight="balanced"))))
    if enabled.get("hist_gradient_boosting", True):
        candidates.append(("hist_gradient_boosting", HistGradientBoostingClassifier(random_state=seed, max_iter=60)))
    if enabled.get("random_forest", True):
        candidates.append(("random_forest", RandomForestClassifier(n_estimators=60, random_state=seed, class_weight="balanced_subsample", n_jobs=-1)))
    if enabled.get("extra_trees", True):
        candidates.append(("extra_trees", ExtraTreesClassifier(n_estimators=60, random_state=seed, class_weight="balanced", n_jobs=-1)))
    models = []
    for name, estimator in candidates:
        estimator.fit(X_train, y_train)
        models.append(TrainedModel(name, estimator, cols))
    return models

