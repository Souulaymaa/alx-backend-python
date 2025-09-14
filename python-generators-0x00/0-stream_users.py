#!/usr/bin/python3

# 0-stream_users.py - generator to stream rows from user_data table one by one


import mysql.connector

DB_NAME = "ALX_prodev"
TABLE_NAME = "user_data"

def stream_users():
 
   # Generator function that fetches rows from user_data one by one.
 
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="alx_user",       # your working user
            password="leetcode",   # your working password
            database=DB_NAME
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM {TABLE_NAME}")

        for row in cursor:
            row['age'] = int(row['age'])  # convert from Decimal to int
            yield row  # yield each row one by one

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# -------------------------
# Quick test: print first 6 rows
# -------------------------
if __name__ == "__main__":
    for i, user in enumerate(stream_users()):
        if i >= 6:
            break
        print(user)
