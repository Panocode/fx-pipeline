import os
import requests
import psycopg2
from clickhouse_driver import Client
from dotenv import load_dotenv

# --- Загрузка переменных окружения ---
load_dotenv()

BASE_CURRENCY = os.getenv("BASE_CURRENCY", "USD")
TARGET_CURRENCIES = os.getenv("TARGET_CURRENCIES", "EUR,RUB,GBP,JPY,CHF,CAD,AUD,NZD,SEK,NOK").split(",")

POSTGRES_CONFIG = {
    "host": os.getenv("POSTGRES_HOST", "postgres"),
    "port": int(os.getenv("POSTGRES_PORT", 5432)),
    "dbname": os.getenv("POSTGRES_DB", "fxdb"),
    "user": os.getenv("POSTGRES_USER", "postgres"),
    "password": os.getenv("POSTGRES_PASSWORD", "postgres")
}

CLICKHOUSE_CONFIG = {
    "host": os.getenv("CLICKHOUSE_HOST", "clickhouse"),
    "port": int(os.getenv("CLICKHOUSE_PORT", 9000)),
    "database": os.getenv("CLICKHOUSE_DB", "fxdb"),
    "user": os.getenv("CLICKHOUSE_USER", "default"),
    "password": os.getenv("CLICKHOUSE_PASSWORD", "")
}

# === FETCH RATES ===
def fetch_rates(base_currency=BASE_CURRENCY, targets=TARGET_CURRENCIES):
    url = "https://api.frankfurter.app/latest"
    params = {"base": base_currency, "symbols": ",".join(targets)}
    resp = requests.get(url, params=params)
    print("STATUS:", resp.status_code)
    print("RAW RESPONSE:", resp.text[:200])
    data = resp.json()
    return data["rates"]

# === LOAD TO POSTGRES ===
def load_postgres(rates, base_currency=BASE_CURRENCY):
    conn = psycopg2.connect(**POSTGRES_CONFIG)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS rates (
            id SERIAL PRIMARY KEY,
            base_currency TEXT,
            target_currency TEXT,
            rate NUMERIC,
            ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    for target, rate in rates.items():
        cur.execute(
            "INSERT INTO rates (base_currency, target_currency, rate) VALUES (%s, %s, %s)",
            (base_currency, target, rate),
        )

    conn.commit()
    cur.close()
    conn.close()
    print("Data saved to Postgres ✅")

# === LOAD TO CLICKHOUSE ===
def load_clickhouse(rates, base_currency=BASE_CURRENCY):
    client = Client(**CLICKHOUSE_CONFIG)

    client.execute(f"""
        CREATE DATABASE IF NOT EXISTS {CLICKHOUSE_CONFIG['database']}
    """)

    client.execute(f"""
        CREATE TABLE IF NOT EXISTS {CLICKHOUSE_CONFIG['database']}.fx_rates (
            ts DateTime DEFAULT now(),
            base_currency String,
            target_currency String,
            rate Float64
        ) ENGINE = MergeTree()
        ORDER BY (ts, base_currency, target_currency)
    """)

    rows = [(base_currency, target, float(rate)) for target, rate in rates.items()]
    client.execute(
        f"INSERT INTO {CLICKHOUSE_CONFIG['database']}.fx_rates (base_currency, target_currency, rate) VALUES",
        rows
    )
    print("Data saved to ClickHouse ✅")

# === MAIN ===
if __name__ == "__main__":
    rates = fetch_rates(BASE_CURRENCY, TARGET_CURRENCIES)
    load_postgres(rates, BASE_CURRENCY)
    load_clickhouse(rates, BASE_CURRENCY)
