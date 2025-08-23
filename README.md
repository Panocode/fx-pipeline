Учебный проект по построению **ETL-пайплайна** для загрузки валютных курсов в PostgreSQL и ClickHouse.  
Сервис скачивает курсы валют (USD → другие валюты) через API, сохраняет их в Postgres (оперативное хранилище), а затем дублирует в ClickHouse (аналитическое хранилище).

---

## Функционал
- Сбор валютных курсов через API.
- Загрузка данных в **PostgreSQL**.
- Репликация данных в **ClickHouse**.
- Планировщик задач (`schedule`).
- Возможность выполнять SQL-запросы к БД.
- Удобный запуск через Docker + Makefile.

---

## Структура проекта

fx-pipeline/
├── etl/ # Python-скрипты для ETL
│ ├── scheduler.py # Планировщик задач
│ └── pipeline.py # Основная логика загрузки
├── sql/
│ ├── postgres_init.sql # Скрипт для инициализации PostgreSQL
│ ├── clickhouse_init.sql# Скрипт для инициализации ClickHouse
│ └── sample_data.sql # Тестовые данные
├── .env.example # Пример переменных окружения
├── docker-compose.yml # Сервисы: Postgres, ClickHouse, ETL
├── Dockerfile # Образ для ETL
├── Makefile # Удобные команды
├── requirements.txt # Python-зависимости
└── README.md # Документация проекта
---

##  Установка и запуск
## Quick Start (TL;DR) <!Быстрый запуск!>
git clone https://github.com/Panocode/fx-pipeline.git
cd fx-pipeline
cp .env.example .env
docker compose up -d


PostgreSQL → localhost:5432

ClickHouse → localhost:9000

ETL запускается автоматически

### 1. Клонируем репозиторий
```bash
git clone https://github.com/Panocode/fx-pipeline.git
cd fx-pipeline
### 2. Настройка окружения
Скопируйте файл окружения и заполните свои значения:

cp .env.example .env
Пример .env:

POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=fxdb
CLICKHOUSE_USER=default
CLICKHOUSE_PASSWORD=
### 3. Запуск проекта Linux|MacOS
make build
make up
###3.1 Запуск проекта Windows(no make)
ps
docker compose build
docker compose up -d
### 4. Проверка сервисов
PostgreSQL доступен на localhost:5432

ClickHouse доступен на localhost:9000

ETL запускается автоматически

### 5. Подключение к БД

make psql   # открыть консоль PostgreSQL
make ch     # открыть консоль ClickHouse
#Тестовые данные
#Чтобы наполнить БД тестовыми данными, можно выполнить:

docker exec -i fx-pipeline-postgres-1 psql -U postgres -d fxdb < sql/sample_data.sql
#Пример запроса
#Последние курсы валют в PostgreSQL:

SELECT base_currency, target_currency, rate, ts
FROM rates
ORDER BY ts DESC
LIMIT 10;

## Автор  
Panocode (Богдан Степан)  
Учебный pet-проект для портфолио.  

## Идеи для доработки
- Подключить **Airflow** вместо `schedule`.
- Сделать дашборд в **Metabase** или **Superset**.
- Добавить unit-тесты.
- Подключить CI/CD (GitHub Actions).