from __future__ import annotations
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DATA.mkdir(parents=True, exist_ok=True)
RNG = np.random.default_rng(2201)

def main():
    rows = []
    for i in range(5000):
        rows.append({
            "source_row_id": i + 1,
            "customer_sk": 100000 + i,
            "customer_name": f"Cust {i}",
            "phone": f"555-{1000 + (i % 9000):04d}",
            "country": RNG.choice(["US", "CA", "GB"]),
        })
    df = pd.DataFrame(rows)
    # Plant 8 NULL_SK and 4 BAD_PHONE
    for i in range(8):
        df.at[i, "customer_sk"] = None
    for i in range(8, 12):
        df.at[i, "phone"] = "NOT-A-PHONE"
    df.to_csv(DATA / "src_customer.csv", index=False)
    print("source rows", len(df))

if __name__ == "__main__":
    main()
