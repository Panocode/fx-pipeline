.PHONY: build up down logs restart psql ch

POSTGRES_CONTAINER=fx-pipeline-postgres-1
CLICKHOUSE_CONTAINER=fx-pipeline-clickhouse-1
DB_NAME=fxdb
DB_USER=postgres

build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

restart: down up

logs:
	docker compose logs -f

psql:
	docker exec -it $(POSTGRES_CONTAINER) psql -U $(DB_USER) -d $(DB_NAME)

ch:
	docker exec -it $(CLICKHOUSE_CONTAINER) clickhouse-client -u default --password
