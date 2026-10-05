from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    average_precision_score,
    roc_auc_score,
    precision_recall_curve,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


class FraudModel:
    """
    IEEE-CIS fraud detection model.

    Target column:
        isFraud

    The model uses a compact, laptop-friendly feature set containing
    transaction, card, address, email and selected V/D/M features.
    """

    def __init__(self):
        self.model = None
        self.feature_names = None
        self.threshold = 0.5
        self.metrics = {}

    def _select_features(self, df):
        preferred = [
            "TransactionAmt",
            "TransactionDT",
            "ProductCD",
            "card1",
            "card2",
            "card3",
            "card4",
            "card5",
            "card6",
            "addr1",
            "addr2",
            "dist1",
            "dist2",
            "P_emaildomain",
            "R_emaildomain",
        ]

        # Add selected V features.
        v_features = [
            c for c in df.columns
            if c.startswith("V") and c[1:].isdigit()
        ]

        # Keep the first 50 V features to control memory/model size.
        v_features = sorted(
            v_features,
            key=lambda x: int(x[1:])
        )[:50]

        selected = [
            c for c in preferred + v_features
            if c in df.columns
        ]

        return df[selected].copy()

    def _build_pipeline(self, X):
        categorical = X.select_dtypes(
            include=["object", "category"]
        ).columns.tolist()

        numerical = [
            c for c in X.columns
            if c not in categorical
        ]

        numeric_pipeline = Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler()),
            ]
        )

        categorical_pipeline = Pipeline(
            steps=[
                (
                    "imputer",
                    SimpleImputer(
                        strategy="most_frequent"
                    ),
                ),
                (
                    "onehot",
                    OneHotEncoder(
                        handle_unknown="ignore",
                        min_frequency=5,
                    ),
                ),
            ]
        )

        preprocessor = ColumnTransformer(
            transformers=[
                ("num", numeric_pipeline, numerical),
                ("cat", categorical_pipeline, categorical),
            ]
        )

        classifier = LogisticRegression(
            max_iter=300,
            class_weight="balanced",
            solver="liblinear",
            random_state=42,
        )

        return Pipeline(
            steps=[
                ("preprocessor", preprocessor),
                ("classifier", classifier),
            ]
        )

    def fit(self, df, target="isFraud"):
        if target not in df.columns:
            raise ValueError(
                f"Expected target column `{target}`."
            )

        y = df[target].astype(int)

        X = self._select_features(df)

        self.feature_names = list(X.columns)

        self.model = self._build_pipeline(X)

        self.model.fit(X, y)

        p = self.model.predict_proba(X)[:, 1]

        self.threshold = self._best_f1_threshold(y, p)

        self.metrics = {
            "roc_auc": float(
                roc_auc_score(y, p)
            ),
            "average_precision": float(
                average_precision_score(y, p)
            ),
            "threshold": float(self.threshold),
            "rows": int(len(df)),
            "features": int(len(self.feature_names)),
            "fraud_count": int(y.sum()),
            "fraud_rate": float(y.mean()),
        }

        return self

    @staticmethod
    def _best_f1_threshold(y, p):
        precision, recall, thresholds = precision_recall_curve(
            y, p
        )

        f1 = (
            2 * precision * recall
            / (precision + recall + 1e-12)
        )

        if len(thresholds) == 0:
            return 0.5

        i = int(np.nanargmax(f1[:-1]))

        return float(thresholds[i])

    def _prepare(self, df):
        if self.feature_names is None:
            raise RuntimeError(
                "Model has not been trained or loaded."
            )

        X = df.copy()

        if "isFraud" in X.columns:
            X = X.drop(columns=["isFraud"])

        if "Class" in X.columns:
            X = X.drop(columns=["Class"])

        X = self._select_features(X)

        for column in self.feature_names:
            if column not in X.columns:
                X[column] = np.nan

        X = X[self.feature_names]

        return X

    def predict_proba(self, df):
        X = self._prepare(df)

        return self.model.predict_proba(X)[:, 1]

    def predict(self, df):
        probabilities = self.predict_proba(df)

        return (
            probabilities >= self.threshold
        ).astype(int)

    def save(self, path):
        Path(path).parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        joblib.dump(self, path)

    def load(self, path):
        obj = joblib.load(path)

        self.__dict__.update(
            obj.__dict__
        )

        return self