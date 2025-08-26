### **Релиз новой версии (V2.0)**
* Добавлен интерфейс (tabulus)
* Добавлено кастомизируемое обновление БД каждые 10 минут с валютным курсом.
* Лёгкий запуск `(bat)` с запуском в docker
* Life-time логи

**Full Changelog**: https://github.com/Panocode/fx-pipeline/commits/v2.0
`update soon:`
`README`
`commentaries`
> docs/comms/readme not actual for v2.0

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
```bash
fx-pipeline/
├─ etl/                  # Python-скрипты для ETL
├─ scheduler.py          # Планировщик задач
├─ pipeline.py           # Основная логика загрузки
├─ sql/
│  ├─ postgres_init.sql   # Скрипт для инициализации PostgreSQL
│  ├─ clickhouse_init.sql # Скрипт для инициализации ClickHouse
│  └─ sample_data.sql     # Тестовые данные
├─ .env.example           # Пример переменных окружения
├─ docker-compose.yml     # Сервисы: Postgres, ClickHouse, ETL
├─ Dockerfile             # Образ для ETL
├─ Makefile               # Удобные команды
├─ requirements.txt       # Python-зависимости
└─ README.md              # Документация проекта
```
---

## Quick Start (TL;DR) Быстрый запуск
```bash
git clone https://github.com/Panocode/fx-pipeline.git
cd fx-pipeline
cp .env.example .env
docker compose up -d          #Поднять весь стек
docker compose up -d sheduler #Перезапустить ETL
Get-Content .\sql\sample_data.sql | docker exec -i fx-pipeline-postgres-1 psql -U postgres -d fxdb #Загрузка тестовых данных PostgreSQL
docker compose exec postgres psql -U postgres -d fxdb #Запуск psql + проверкуа данных в PostgreSQL
docker compose exec clickhouse clickhouse-client #Запуск ClickHouse
```
## Пример запроса к БД
```bash
#Последние 10 записей
SELECT base_currency, target_currency, rate, ts 
FROM rates
ORDER BY ts DESC
LIMIT 10;
```
## Другое
```bash
PostgreSQL → localhost:5432
ClickHouse → localhost:9000
ETL запускается автоматически
```
###  Установка и запуск >1. Клонируем репозиторий
```bash
git clone https://github.com/Panocode/fx-pipeline.git
cd fx-pipeline
```
### 2. Настройка окружения
Скопируйте файл окружения и заполните свои значения:
cp .env.example .env
Пример .env:
```bash
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=fxdb
CLICKHOUSE_USER=default
CLICKHOUSE_PASSWORD=
```
### 3. Запуск проекта Linux|MacOS
```bash
make build
make up
```
### 3.1 Запуск проекта Windows(no make)
ps
```bash
docker compose build
docker compose up -d # Поднять весь стек
docker compose up -d scheduler # Перезапуск ETL
```
### 4. Проверка сервисов
```bash
PostgreSQL доступен на localhost:5432

ClickHouse доступен на localhost:9000

ETL запускается автоматически
```
### 5. Подключение к БД
```bash
make psql   # открыть консоль PostgreSQL
make ch     # открыть консоль ClickHouse
#Тестовые данные
#Чтобы наполнить БД тестовыми данными, можно выполнить:

docker exec -i fx-pipeline-postgres-1 psql -U postgres -d fxdb < sql/sample_data.sql
#Пример запроса
#Последние курсы валют в PostgreSQL:

#Последние 10 записей
SELECT base_currency, target_currency, rate, ts 
FROM rates
ORDER BY ts DESC
LIMIT 10;
```
### 6. Примеры запросов к БД
```bash 
#Все курсы за последние 2 дня
SELECT base_currency, target_currency, rate, ts 
FROM rates
WHERE ts >= now() - interval '2 days'
ORDER BY ts DESC;

#Средний курс за 7 дней
SELECT base_currency, target_currency, ROUND(AVG(rate),4) AS avg_rate 
FROM rates
WHERE ts >= now() - interval '7 days'
GROUP BY base_currency, target_currency
ORDER BY avg_rate DESC;

#Минимальный и максимальный курс за неделю
SELECT base_currency, target_currency, 
       MIN(rate) AS min_rate,
       MAX(rate) AS max_rate
FROM rates
WHERE ts >= now() - interval '7 days'
GROUP BY base_currency, target_currency
ORDER BY base_currency, target_currency;

#Кол-во записей по каждоой валютной паре
SELECT base_currency, target_currency, COUNT(*) AS records_count 
FROM rates
GROUP BY base_currency, target_currency
ORDER BY records_count DESC;
```
## Автор  
Автор: [Panocode](https://github.com/Panocode)  
Учебный pet-проект для портфолио.  

## Идеи для доработки
```bash
- Подключить **Airflow** вместо `schedule`.
- Сделать дашборд в **Metabase** или **Superset**.
- Добавить unit-тесты.
- Подключить CI/CD (GitHub Actions).
```
