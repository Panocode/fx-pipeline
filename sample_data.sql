CREATE TABLE IF NOT EXISTS rates (
    id SERIAL PRIMARY KEY,
    base_currency VARCHAR(3) NOT NULL,
    target_currency VARCHAR(3) NOT NULL,
    rate NUMERIC(12,6) NOT NULL,
    ts TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Тестовые данные
INSERT INTO rates (base_currency, target_currency, rate, ts) VALUES
('USD', 'EUR', 0.9234, NOW() - INTERVAL '2 days'),
('USD', 'GBP', 0.8123, NOW() - INTERVAL '2 days'),
('USD', 'JPY', 148.25, NOW() - INTERVAL '2 days'),
('USD', 'CHF', 0.9021, NOW() - INTERVAL '2 days'),

('USD', 'EUR', 0.9267, NOW() - INTERVAL '1 days'),
('USD', 'GBP', 0.8199, NOW() - INTERVAL '1 days'),
('USD', 'JPY', 147.88, NOW() - INTERVAL '1 days'),
('USD', 'CHF', 0.9054, NOW() - INTERVAL '1 days'),

('USD', 'EUR', 0.9285, NOW()),
('USD', 'GBP', 0.8241, NOW()),
('USD', 'JPY', 147.55, NOW()),
('USD', 'CHF', 0.9072, NOW());