import requests
import psycopg2
from clickhouse_driver import Client
from datetime import datetime

# API курсы валют
url = "https://api.exchangerate.host/latest?base=USD&symbols=EUR,GBP"
resp = requests.get(url).json()
rates = resp["rates"]

# PostgreSQL
pg_conn = psycopg2.connect("dbname=fx user=user password=pass host=localhost")
pg_cur = pg_conn.cursor()

# ClickHouse
ch_client = Client(host="localhost")

for cur, rate in rates.items():
    ts = datetime.utcnow()

    pg_cur.execute("INSERT INTO fx_rates (base_currency, target_currency, rate, ts) VALUES (%s, %s, %s, %s)",
                   ("USD", cur, rate, ts))
    pg_conn.commit()

    ch_client.execute("INSERT INTO fx_rates VALUES", [("USD", cur, float(rate), ts)])

print("ETL done.")