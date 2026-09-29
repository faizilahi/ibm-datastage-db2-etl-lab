from __future__ import annotations
import json
import pandas as pd

def transform(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    good, rejects = [], []
    for _, r in df.iterrows():
        if pd.isna(r["customer_sk"]):
            rejects.append(_rej(r, "NULL_SK"))
        elif not str(r["phone"]).startswith("555-"):
            rejects.append(_rej(r, "BAD_PHONE"))
        else:
            good.append(r.to_dict())
    return pd.DataFrame(good), pd.DataFrame(rejects)

def _rej(r, code):
    return {
        "source_row_id": int(r["source_row_id"]),
        "reject_code": code,
        "payload_json": json.dumps({k: (None if pd.isna(v) else v) for k, v in r.items()}),
    }
