from InquirerPy import inquirer
import os
import psycopg2
from clickhouse_driver import Client
from dotenv import load_dotenv
from tabulate import tabulate
import time

# --- Загрузка переменных окружения ---
load_dotenv()

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

BASE_CURRENCY = "USD"
TARGET_CURRENCIES = ["EUR", "GBP", "JPY", "CHF", "CAD", "AUD", "CNY", "NZD", "SEK"]


# --- Ожидание готовности баз ---
def wait_for_postgres():
    for _ in range(10):
        try:
            conn = psycopg2.connect(**POSTGRES_CONFIG)
            conn.close()
            print("Postgres готов ✅")
            return
        except psycopg2.OperationalError:
            print("Ожидание Postgres...")
            time.sleep(3)
    print("Не удалось подключиться к Postgres 😢")
    exit(1)

def wait_for_clickhouse():
    for _ in range(10):
        try:
            client = Client(**CLICKHOUSE_CONFIG)
            client.execute("SELECT 1")
            print("ClickHouse готов ✅")
            return
        except Exception:
            print("Ожидание ClickHouse...")
            time.sleep(3)
    print("Не удалось подключиться к ClickHouse 😢")
    exit(1)


# --- Подключения ---
def connect_postgres():
    return psycopg2.connect(**POSTGRES_CONFIG)

def connect_clickhouse():
    return Client(**CLICKHOUSE_CONFIG)


# --- Работа с таблицами ---
def show_postgres_tables():
    conn = connect_postgres()
    cur = conn.cursor()
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public';")
    tables = [t[0] for t in cur.fetchall()]
    conn.close()
    return tables

def show_clickhouse_tables():
    client = connect_clickhouse()
    return [t[0] for t in client.execute(f"SHOW TABLES FROM {CLICKHOUSE_CONFIG['database']}")]


# --- Запросы ---
def query_postgres(query):
    conn = connect_postgres()
    cur = conn.cursor()
    cur.execute(query)
    try:
        rows = cur.fetchall()
        headers = [desc[0] for desc in cur.description]
    except psycopg2.ProgrammingError:
        rows = []
        headers = []
    conn.commit()
    conn.close()
    return headers, rows

def query_clickhouse(query):
    client = connect_clickhouse()
    try:
        rows = client.execute(query)
        if rows:
            headers = [col[0] for col in client.execute(f"DESCRIBE TABLE {CLICKHOUSE_CONFIG['database']}.fx_rates")]
        else:
            headers = []
    except Exception as e:
        rows = [[f"Ошибка: {e}"]]
        headers = []
    return headers, rows


def print_table(headers, rows):
    if not rows:
        print("Нет данных или запрос не вернул строк.")
        return
    print("\n" + tabulate(rows, headers=headers, tablefmt="fancy_grid"))


def main():
    wait_for_postgres()
    wait_for_clickhouse()

    while True:
        choice = inquirer.select(
            message="Выберите базу данных:",
            choices=["PostgreSQL", "ClickHouse", "Выход"],
            default="PostgreSQL"
        ).execute()

        if choice == "Выход":
            print("До свидания 👋")
            break

        if choice == "PostgreSQL":
            action = inquirer.select(
                message="Что сделать?",
                choices=["Посмотреть таблицы", "Ввести свой SQL-запрос", "Назад"]
            ).execute()

            if action == "Посмотреть таблицы":
                tables = show_postgres_tables()
                if not tables:
                    print("Нет таблиц в PostgreSQL")
                    continue
                table = inquirer.select(
                    message="Выберите таблицу:",
                    choices=tables + ["Назад"]
                ).execute()
                if table == "Назад":
                    continue
                headers, rows = query_postgres(f"SELECT * FROM {table} LIMIT 10;")
                print_table(headers, rows)

            elif action == "Ввести свой SQL-запрос":
                sql = inquirer.text(message="Введите SQL-запрос:").execute()
                headers, rows = query_postgres(sql)
                print_table(headers, rows)

        elif choice == "ClickHouse":
            action = inquirer.select(
                message="Что сделать?",
                choices=["Посмотреть таблицы", "Ввести свой SQL-запрос", "Назад"]
            ).execute()

            if action == "Посмотреть таблицы":
                try:
                    tables = show_clickhouse_tables()
                except Exception as e:
                    print(f"Не удалось подключиться к ClickHouse: {e}")
                    continue
                if not tables:
                    print("Нет таблиц в ClickHouse")
                    continue
                table = inquirer.select(
                    message="Выберите таблицу:",
                    choices=tables + ["Назад"]
                ).execute()
                if table == "Назад":
                    continue
                headers, rows = query_clickhouse(f"SELECT * FROM {CLICKHOUSE_CONFIG['database']}.{table} LIMIT 10")
                print_table(headers, rows)

            elif action == "Ввести свой SQL-запрос":
                sql = inquirer.text(message="Введите SQL-запрос:").execute()
                headers, rows = query_clickhouse(sql)
                print_table(headers, rows)


if __name__ == "__main__":
    main()
