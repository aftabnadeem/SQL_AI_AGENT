from llm import generate_query
from db import execute_sql

def generate_v1_query(schema, question, model="gemini-3.5-flash"):
    prompt = f"""
    Your an postgresql expert. 
    You are given a database schema and a question, you need to answer the question using the database schema.

    Schema = 
    {schema}

    Question = {question}

    Strictly answer only using postgresql query.
    no preceding ```sql or nothing just sql command or query which can be executed directly in postgresql.

    example asnwer: 
    SELECT * FROM coffee_sales WHERE month_name = 'May';

    """

    query = generate_query(model, prompt)

    return list(execute_sql(query, fetch=True)), query

