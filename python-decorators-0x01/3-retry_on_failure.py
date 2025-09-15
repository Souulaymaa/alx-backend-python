import time
import sqlite3 
import functools

#### paste your with_db_decorator here
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db") # opens a connection to users.db
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close() # closes the database connection
    return wrapper

def retry_on_failure(retries=3, delay=2):
    def decorator2(func):
        @functools.wraps(func)
        def wrapper(conn, *args, **kwargs):
            for tries in range(0, retries):
                try:
                    result = func(conn, *args, **kwargs)
                    return result
                except Exception as e:
                    print(f"Transaction attempt {tries+1} failed: {e}")
                    conn.rollback()
                    if tries < retries - 1:
                        time.sleep(delay)
                    else:
                        raise   # after last try, raise the error
        return wrapper
    return decorator2

@with_db_connection
@retry_on_failure(retries=3, delay=1)

def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure

users = fetch_users_with_retry()
print(users)