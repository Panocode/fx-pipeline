CREATE TABLE IF NOT EXISTS fx_rates
(
    base_currency String,
    target_currency String,
    rate Float64,
    ts DateTime
)
ENGINE = MergeTree()
ORDER BY ts;