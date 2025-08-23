import requests
import psycopg2
from clickhouse_driver import Client

# --- Настройки ---
BASE_CURRENCY = "USD"
CURRENCIES = ["EUR", "RUB"]  # список нужных валют


# === FETCH RATES ===
def fetch_rates(base_currency=BASE_CURRENCY, targets=CURRENCIES):
    url = "https://api.frankfurter.app/latest"
    params = {"base": base_currency, "symbols": ",".join(targets)}
    resp = requests.get(url, params=params)

    print("STATUS:", resp.status_code)
    print("RAW RESPONSE:", resp.text[:200])

    data = resp.json()
    return data["rates"]


# === LOAD TO POSTGRES ===
def load_postgres(rates, base_currency=BASE_CURRENCY):
    conn = psycopg2.connect(
        dbname="fxdb",
        user="postgres",
        password="postgres",
        host="localhost",   # ⚠️ если запускать из контейнера — поменять на "postgres"
        port=5432,
    )
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS rates (
            base_currency TEXT,
            target_currency TEXT,
            rate NUMERIC,
            date DATE DEFAULT CURRENT_DATE
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
    client = Client(host="localhost")  # ⚠️ если из контейнера — поменять на "clickhouse"

    client.execute("""
        CREATE TABLE IF NOT EXISTS fxdb.fx_rates (
            base_currency String,
            target_currency String,
            rate Float64,
            date Date DEFAULT today()
        ) ENGINE = MergeTree()
        ORDER BY (date, base_currency, target_currency)
    """)

    rows = [(base_currency, target, float(rate)) for target, rate in rates.items()]
    client.execute(
        "INSERT INTO fxdb.fx_rates (base_currency, target_currency, rate) VALUES",
        rows,
    )
    print("Data saved to ClickHouse ✅")


# === MAIN ===
if __name__ == "__main__":
    rates = fetch_rates(BASE_CURRENCY, CURRENCIES)
    load_postgres(rates, BASE_CURRENCY)
    load_clickhouse(rates, BASE_CURRENCY)