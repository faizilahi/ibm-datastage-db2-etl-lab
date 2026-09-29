import numpy as np, pandas as pd
from pathlib import Path
RNG=np.random.default_rng(13)
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/"data"; DATA.mkdir(parents=True, exist_ok=True)
rows=[]
for i in range(1,251):
  email = f"user{i}@example.com" if RNG.random()>0.08 else ""
  rows.append({"customer_id":i,"name":f"Cust {i}","email":email,"region":RNG.choice(["NAM","EU","APAC"]),
    "balance":round(float(RNG.uniform(-50,5000)),2)})
pd.DataFrame(rows).to_csv(DATA/"source_customers.csv",index=False)
print("Wrote DataStage source")

