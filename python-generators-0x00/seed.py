#!/usr/bin/python3
"""
seed.py - Setup ALX_prodev database, create table user_data,
and insert sample data directly from Python (no CSV needed).
"""

import mysql.connector
import uuid

DB_NAME = "ALX_prodev"
TABLE_NAME = "user_data"

# -------------------------
# Connect to MySQL server
# -------------------------
def connect_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="alx_user",       # your working user
            password="leetcode"    # your working password
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# -------------------------
# Create database if missing
# -------------------------
def create_database(connection):
    cursor = connection.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME};")
    cursor.close()

# -------------------------
# Connect directly to ALX_prodev
# -------------------------
def connect_to_prodev():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="alx_user",
            password="leetcode",
            database=DB_NAME
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# -------------------------
# Create user_data table
# -------------------------
def create_table(connection):
    cursor = connection.cursor()
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            user_id CHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL NOT NULL,
            INDEX (user_id)
        );
    """)
    connection.commit()
    cursor.close()
    print("Table user_data created successfully")

# -------------------------
# Insert sample data
# -------------------------
def insert_data(connection):
    sample_data = [
        {"name": "Dan Altenwerth Jr.", "email": "Molly59@gmail.com", "age": 67},
        {"name": "Glenda Wisozk", "email": "Miriam21@gmail.com", "age": 119},
        {"name": "Daniel Fahey IV", "email": "Delia.Lesch11@hotmail.com", "age": 49},
        {"name": "Ronnie Bechtelar", "email": "Sandra19@yahoo.com", "age": 22},
        {"name": "Alma Bechtelar", "email": "Shelly_Balistreri22@hotmail.com", "age": 102},
        {"name": "Jonathon Jones", "email": "Jody.Quigley-Ziemann33@yahoo.com", "age": 116}
    ]

    cursor = connection.cursor()
    for row in sample_data:
        user_id = str(uuid.uuid4())
        cursor.execute(f"""
            INSERT INTO {TABLE_NAME} (user_id, name, email, age)
            VALUES (%s, %s, %s, %s)
        """, (user_id, row["name"], row["email"], row["age"]))
    connection.commit()
    cursor.close()
    print("Sample data inserted successfully")

# -------------------------
# Run everything
# -------------------------
if __name__ == "__main__":
    connection = connect_db()
    if connection:
        print("Connected to MySQL server")
        create_database(connection)
        connection.close()

        connection = connect_to_prodev()
        if connection:
            create_table(connection)
            insert_data(connection)
            connection.close()
            print("Seeded database successfully")
