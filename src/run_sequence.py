from __future__ import annotations
import json, sys
from pathlib import Path
import pandas as pd
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from sequence_runner import run_sequence, upsert, bad_rerun, load_seq

DATA, OUT, REJ, JOBS = ROOT / "data", ROOT / "output", ROOT / "rejects", ROOT / "jobs"
OUT.mkdir(parents=True, exist_ok=True)
REJ.mkdir(parents=True, exist_ok=True)

def main():
    src = pd.read_csv(DATA / "src_customer.csv")
    cfg = load_seq(JOBS / "seq_customer_daily.json")
    first = run_sequence(src, cfg, force_continue=False)
    first["rejects"].to_csv(REJ / "customer_rejects.csv", index=False)
    # Forced continue after triage
    cont = run_sequence(src, cfg, force_continue=True)
    target = upsert(pd.DataFrame(), cont["good"])
    clean_count = len(target)
    messed = bad_rerun(target, cont["good"])
    summary = {
        "reject_count": first["reject_count"],
        "sequence_stopped_first_run": first["stopped"],
        "null_sk_rejects": int((first["rejects"]["reject_code"] == "NULL_SK").sum()),
        "bad_phone_rejects": int((first["rejects"]["reject_code"] == "BAD_PHONE").sum()),
        "clean_target_count": clean_count,
        "bad_rerun_count": int(len(messed)),
        "inflation_rows": int(len(messed) - clean_count),
    }
    target.to_csv(OUT / "db2_customer_daily.csv", index=False)
    messed.to_csv(OUT / "db2_customer_daily_bad_rerun.csv", index=False)
    pd.DataFrame([summary]).to_csv(OUT / "sequence_summary.csv", index=False)
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
