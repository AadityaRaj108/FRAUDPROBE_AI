import argparse
import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1])
)

import pandas as pd

from src.model import FraudModel


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--data",
        required=True,
    )

    parser.add_argument(
        "--sample",
        type=int,
        default=100000,
        help="Number of rows to use for laptop-friendly training",
    )

    parser.add_argument(
        "--output",
        default="artifacts/fraud_model.joblib",
    )

    args = parser.parse_args()

    print("Loading dataset...")

    df = pd.read_csv(
        args.data,
        nrows=args.sample,
    )

    print(
        f"Loaded {len(df):,} rows "
        f"and {len(df.columns):,} columns."
    )

    if "isFraud" not in df.columns:
        raise ValueError(
            "Expected target column `isFraud`."
        )

    print(
        f"Fraud transactions: "
        f"{df['isFraud'].sum():,}"
    )

    print("Training model...")

    model = FraudModel().fit(
        df,
        target="isFraud",
    )

    model.save(args.output)

    print()
    print("=" * 50)
    print("FRAUDPROBE AI MODEL TRAINED")
    print("=" * 50)
    print("Saved:", args.output)
    print("Metrics:", model.metrics)
    print("Features:", len(model.feature_names))


if __name__ == "__main__":
    main()