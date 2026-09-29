from __future__ import annotations
import json
from pathlib import Path
import pandas as pd
from transform import transform

def run_sequence(src: pd.DataFrame, seq_cfg: dict, force_continue: bool = False) -> dict:
    good, rejects = transform(src)
    threshold = seq_cfg["reject_threshold"]
    stopped = len(rejects) > threshold and not force_continue
    return {
        "good": good,
        "rejects": rejects,
        "stopped": stopped,
        "reject_count": int(len(rejects)),
        "good_count": int(len(good)),
    }

def upsert(target: pd.DataFrame, incoming: pd.DataFrame) -> pd.DataFrame:
    if target.empty:
        return incoming.copy()
    # simulate primary key on customer_sk
    keys = set(incoming["customer_sk"].tolist())
    kept = target[~target["customer_sk"].isin(keys)]
    return pd.concat([kept, incoming], ignore_index=True)

def bad_rerun(target: pd.DataFrame, full_extract_good: pd.DataFrame) -> pd.DataFrame:
    """Ops mistake: append without dedupe."""
    return pd.concat([target, full_extract_good.head(3)], ignore_index=True)

def load_seq(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))
