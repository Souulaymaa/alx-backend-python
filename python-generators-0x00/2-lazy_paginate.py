#!/usr/bin/python3

# 2-lazy_paginate.py - Simulte fetching paginated data from the users database using a generator to lazily load each page


import mysql.connector
seed = __import__('seed')

def paginate_users(page_size, offset):
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()
    return rows


def lazypaginate(page_size):
    offset = 0
    while True:
        pages = paginate_users(page_size, offset)
        if not pages:    # empty list evaluates to False
            break       # stop the loop, no more pages
        yield pages
        offset += page_size