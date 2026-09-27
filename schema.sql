CREATE TABLE IF NOT EXISTS coffee_sales (
    id BIGSERIAL PRIMARY KEY,
    hour_of_day SMALLINT CHECK (hour_of_day BETWEEN 0 AND 23),
    cash_type VARCHAR(20),
    money NUMERIC(10, 2),
    coffee_name VARCHAR(100),
    time_of_day VARCHAR(50),
    weekday VARCHAR(20),
    month_name VARCHAR(20),
    weekdaysort SMALLINT,
    monthsort SMALLINT,
    sale_date DATE
);