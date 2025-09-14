#!/usr/bin/python3

# 1-batch_processing.py - generator that fetches and processes data in batches from the users database

import mysql.connector

DB_NAME = "ALX_prodev"
TABLE_NAME = "user_data"

def stream_users_in_batches(batch_size):
# Generator that streams rows from user_data table in batches of batch_size.
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="alx_user",       # your working user
            password="leetcode",   # your working password
            database=DB_NAME
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM {TABLE_NAME}")

        temp_batch = []     #temporary list to store the rows until we reach the size
        for row in cursor:
            row['age'] = int(row['age'])  # convert from Decimal to int
            temp_batch.append(row)
            if len(temp_batch) == batch_size:
                yield temp_batch
                temp_batch = []
        if temp_batch:      #the remaining rows (less than the size)
            yield temp_batch
    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
    return 

def batch_processing(batch_size):
    #Processes users in batches and yields users older than 25.
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            # unpack the dictionary values for clarity
            user_id = user['user_id']
            name = user['name']
            email = user['email']
            age = user['age']

            if age > 25:
                yield {
                    'user_id': user_id,
                    'name': name,
                    'email': email,
                    'age': age
                }


"""
# Quick test: print first 6 rows
#In order to test you need to comment out the finally block in the stream_users_in_batches(batch_size) func

if __name__ == "__main__":
    connection = mysql.connector.connect(
    host="localhost",
    user="alx_user",
    password="leetcode",
    database="ALX_prodev"
)
  # connection needed to close later
    try:
        for i, user in enumerate(batch_processing(batch_size=3)):
            if i >= 6:
                break
            print(user)
    finally:
        connection.close()
"""
