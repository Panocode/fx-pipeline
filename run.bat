@echo off
chcp 65001
REM
docker compose up -d

REM
echo Ожидание Postgres и ClickHouse...
timeout /t 5 >nul

REM
echo Загрузка текущих курсов...
docker compose run --rm scheduler python etl/etl.py

REM
docker compose run --rm scheduler python cli.py

REM
echo CLI завершён. Контейнеры продолжают работать в фоне.
pause