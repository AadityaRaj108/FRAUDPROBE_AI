from pathlib import Path
import numpy as np
import pandas as pd

def main(n=100000, out="data/demo_transactions.csv"):
    rng = np.random.default_rng(42)
    X = rng.normal(size=(n, 28))
    amount = np.exp(rng.normal(3.2, 1.2, n))
    time = np.sort(rng.integers(0, 172800, n))
    # Synthetic demo data only; deliberately not used as a substitute for a real benchmark dataset.
    signal = (0.7*X[:,0] - 0.4*X[:,3] + 0.5*X[:,7] + np.log1p(amount)/8)
    prob = 1/(1+np.exp(-(signal-2.7)))
    y = (rng.random(n) < prob*0.015).astype(int)
    df = pd.DataFrame(X, columns=[f"V{i}" for i in range(1,29)])
    df.insert(0,"Time",time)
    df["Amount"] = amount
    df["Class"] = y
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out,index=False)
    print(f"Wrote {n:,} rows to {out}")

if __name__ == "__main__":
    main()
