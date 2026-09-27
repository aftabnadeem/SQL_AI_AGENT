from v1_query import generate_v1_query
from v2_query import generate_v2_query

schema = """
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

question = """
what is the total revenue for the payment type using card?
"""

v1_answer, v1_query = generate_v1_query(schema, question, model="gemini-3.5-flash")

v2_answer, v2_query = generate_v2_query(schema, question, model="gemini-3.5-flash", v1_answer=v1_answer, v1_query=v1_query) 

print("---------------------------------------")
print("             VERSION 1")
print("Version1 query:",{v1_query})
print("Version1 answer:", {v1_answer})
print("---------------------------------------")

print("---------------------------------------")
print("             VERSION 2")
print("Version2 query:", {v2_query})
print("Version2 answer:", {v2_answer})
print("---------------------------------------")