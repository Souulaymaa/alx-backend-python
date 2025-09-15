import time
import sqlite3 
import functools


query_cache = {}

def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db") # opens a connection to users.db
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close() # closes the database connection
    return wrapper


def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        # Extract query string
        query = kwargs.get("query") if "query" in kwargs else (args[0] if args else None)
        # If query result is cached, return it
        if query in query_cache:
            print(f"Using cached result for query: {query}")
            return query_cache[query]
        # Otherwise, execute the query and cache the result
        result = func(conn, *args, **kwargs)
        query_cache[query] = result
        print(f"Query executed and cached: {query}")
        return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")