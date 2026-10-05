import pandas as pd
import numpy as np

def normalize_columns(df):
    out = df.copy()
    out.columns = [str(c).strip() for c in out.columns]
    return out

def load_csv_sample(file_obj, nrows=5000):
    return normalize_columns(pd.read_csv(file_obj, nrows=nrows))

def predict_csv_in_chunks(file_obj, model, chunksize=50000):
    outputs = []
    for chunk in pd.read_csv(file_obj, chunksize=chunksize):
        chunk = normalize_columns(chunk)
        pred = model.predict_proba(chunk)
        scored = chunk.copy()
        scored["fraud_probability"] = pred
        scored["risk_score"] = np.round(pred * 100).astype(int)
        scored["risk_band"] = pd.cut(
            scored["risk_score"],
            bins=[-1, 24, 49, 74, 100],
            labels=["LOW","MEDIUM","HIGH","CRITICAL"]
        ).astype(str)
        outputs.append(scored)
    return pd.concat(outputs, ignore_index=True) if outputs else pd.DataFrame()
