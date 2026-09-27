# db.py
import psycopg
from psycopg.rows import dict_row
from config import DB_CONFIG

def execute_sql(query: str, params: tuple | list | dict = None, fetch: bool = False):
    """
    Executes a SQL query against PostgreSQL using Psycopg 3.
    
    :param query: SQL string (use %s placeholders for parameterization)
    :param params: Values to safely bind to the placeholders
    :param fetch: If True, returns query results as a list of dicts
    """
    # Unpack DB_CONFIG kwargs directly into psycopg.connect
    with psycopg.connect(**DB_CONFIG, row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            
            if fetch:
                return cur.fetchall()
            
            # Non-fetch operations commit automatically upon exiting the 'conn' block
            return None