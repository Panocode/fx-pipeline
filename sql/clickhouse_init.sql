CREATE DATABASE IF NOT EXISTS fxdb;

CREATE TABLE IF NOT EXISTS fxdb.fx_rates
(
    ts DateTime DEFAULT now(),
    base_currency String,
    target_currency String,
    rate Float64
)
ENGINE = MergeTree()
ORDER BY (ts, base_currency, target_currency);