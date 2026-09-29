# DataStage Sequence Failure and the Reject Link

[Faiz Elahi](https://www.linkedin.com/in/faizilahi) — [pendataco.com](https://pendataco.com) — [github.com/faizilahi](https://github.com/faizilahi)

Synthetic data only. No vendor-customer employment claim.

Job sequence `seq_customer_daily` failed on the DB2 upsert after the transform
stage passed **12** rows down the reject link (null `customer_sk`, bad phone).
Ops reran without clearing rejects and double-loaded **3** previously good rows.

## Job sequence

`jobs/seq_customer_daily.json` orders: extract → transform → reject_capture →
db2_upsert → control_total. The simulator in `src/sequence_runner.py` stops the
sequence when reject count exceeds threshold **10** unless `FORCE_CONTINUE=1`.

## Reject rows

Reject link schema: `source_row_id`, `reject_code`, `payload_json`. Planted
rejects: **8** `NULL_SK`, **4** `BAD_PHONE`. They land in `rejects/customer_rejects.csv`.

## The rerun

Correct rerun: quarantine rejects, replay only clean ids, assert target count
matches control. Bad rerun replayed the full extract and inflated DB2 by **3**.
Worked clean target count **4,988**; bad rerun count **4,991**.

```powershell
pip install -r requirements.txt
python scripts/generate_synthetic_data.py
python src/run_sequence.py
```
