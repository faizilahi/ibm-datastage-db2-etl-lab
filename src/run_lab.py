from pathlib import Path
import sqlite3, pandas as pd
ROOT=Path(__file__).resolve().parents[1]
DATA,OUT=ROOT/"data",ROOT/"output"; OUT.mkdir(parents=True, exist_ok=True)
src=pd.read_csv(DATA/"source_customers.csv")
# Transform stage + reject link
ok=src[src["email"].astype(str).str.len()>0].copy()
rej=src[src["email"].astype(str).str.len()==0].copy(); rej["reject_reason"]="missing_email"
ok["email"]=ok["email"].str.lower()
ok=ok[["customer_id","name","email","region","balance"]]
# Load stage into Db2 stand-in
con=sqlite3.connect(ROOT/"db2_standin.db")
con.execute("DROP TABLE IF EXISTS customers")
con.execute("CREATE TABLE customers (customer_id INTEGER PRIMARY KEY, name TEXT, email TEXT, region TEXT, balance REAL)")
ok.to_sql("customers", con, if_exists="append", index=False)
summary=pd.read_sql("SELECT region, COUNT(*) AS customers, ROUND(SUM(balance),2) AS balance FROM customers GROUP BY 1 ORDER BY 1", con)
summary.to_csv(OUT/"summary.csv",index=False)
rej.to_csv(OUT/"rejects.csv",index=False)
pd.DataFrame([{"extracted":len(src),"loaded":len(ok),"rejected":len(rej)}]).to_csv(OUT/"control_totals.csv",index=False)
con.close(); print(summary)

