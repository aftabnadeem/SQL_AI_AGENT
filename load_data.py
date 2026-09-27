import csv
from datetime import datetime
import psycopg
from config import DB_CONFIG

CREATE_TABLE_SQL = """
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
"""

INSERT_SQL = """
INSERT INTO coffee_sales (
    hour_of_day,
    cash_type,
    money,
    coffee_name,
    time_of_day,
    weekday,
    month_name,
    weekdaysort,
    monthsort,
    sale_date
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
"""

def clean_row(row: dict) -> tuple:
    """Normalize and cast CSV string values to proper Python/PostgreSQL types."""
    # Handle possible casing differences from CSV headers
    def get_val(*keys):
        for k in keys:
            if k in row and row[k] != "":
                return row[k].strip()
        return None

    # Parse date (handles common formats like YYYY-MM-DD or MM/DD/YYYY)
    raw_date = get_val("Date", "date")
    parsed_date = None
    if raw_date:
        for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y"):
            try:
                parsed_date = datetime.strptime(raw_date, fmt).date()
                break
            except ValueError:
                continue

    return (
        int(get_val("hour_of_day")) if get_val("hour_of_day") is not None else None,
        get_val("cash_type"),
        float(get_val("money")) if get_val("money") is not None else None,
        get_val("coffee_name"),
        get_val("Time_of_Day", "time_of_day"),
        get_val("Weekday", "weekday"),
        get_val("Month_name", "month_name"),
        int(get_val("Weekdaysort", "weekdaysort")) if get_val("Weekdaysort", "weekdaysort") is not None else None,
        int(get_val("Monthsort", "monthsort")) if get_val("Monthsort", "monthsort") is not None else None,
        parsed_date,
    )

def load_first_100_rows(csv_file_path: str):
    rows_to_insert = []

    # Read exactly 100 data rows
    with open(csv_file_path, mode="r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            if i >= 100:
                break
            rows_to_insert.append(clean_row(row))

    if not rows_to_insert:
        print("No rows found in CSV.")
        return

    # Connect and insert in a single transaction
    with psycopg.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            # 1. Ensure table exists
            cur.execute(CREATE_TABLE_SQL)
            
            # 2. Batch insert using executemany
            cur.executemany(INSERT_SQL, rows_to_insert)
            
        # Transaction commits automatically on exiting the context manager
        print(f"Successfully inserted {len(rows_to_insert)} rows into 'coffee_sales'.")

if __name__ == "__main__":
    load_first_100_rows("Coffe_sales.csv")