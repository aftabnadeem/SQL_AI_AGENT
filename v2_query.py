from llm import generate_query
from db import execute_sql
import json

def generate_v2_query(schema, question, model="gemini-3.5-flash", v1_answer=None, v1_query=None):
    prompt = f"""
    Your an postgresql expert and query reviewer. 
    You are given a database schema and a question, and also the answer given by a previous llm to this question, 
    and result after excecuting the query,

    Schema = 
    {schema}

    Question = {question}
    query given by previous llm = {v1_query}
    result after excecuting the query = {v1_answer}

    Strictly answer only using postgresql query.
    - return strictly in this json format:
        {{
            "feedback": "the join table was incorrect or the query was incorrect",
            "query": "SELECT * FROM coffee_sales WHERE month_name = 'May';",
            "incorrect_query": True or False
        }}
    - query key should not have no preceding ```sql or nothing just sql command or query which can be executed directly in postgresql.
    - Answer only if required else return back the query given by previous llm.


    """

    query = generate_query(model, prompt)

    print("v2 query")
    print(query)

    # convert query string to dictionary.
    query_dict = json.loads(query)

    if not query_dict["incorrect_query"]:
        return v1_answer, v1_query

    return list(execute_sql(query, fetch=True)), query

