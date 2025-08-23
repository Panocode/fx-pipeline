-- Создание таблицы rates
CREATE TABLE IF NOT EXISTS rates (
    base_currency VARCHAR(3),
    target_currency VARCHAR(3),
    rate NUMERIC(10,4),
    ts TIMESTAMP DEFAULT now()
);

-- Пример данных
INSERT INTO rates (base_currency, target_currency, rate, ts) VALUES
('USD', 'EUR', 0.9123, now() - interval '2 day'),
('USD', 'GBP', 0.8121, now() - interval '2 day'),
('USD', 'JPY', 146.23, now() - interval '1 day'),
('USD', 'EUR', 0.9150, now() - interval '1 day'),
('USD', 'GBP', 0.8150, now()),
('USD', 'JPY', 146.50, now());