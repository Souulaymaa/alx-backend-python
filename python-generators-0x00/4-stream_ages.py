#!/usr/bin/python3

# use a generator to compute a memory-efficient aggregate function i.e average age for a large dataset

import seed

# a generator stream_user_ages() that yields user ages one by one.
def stream_user_ages():
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data")
    for row in cursor:
        yield row['age']
    cursor.close()
    connection.close()

def average_age():
    total_age = 0
    count = 0
    for ages in stream_user_ages():
        total_age += ages
        count += 1
    if count > 0:
        average = total_age / count
    print(f"Average age of users: {average:.2f}")


# -------------------------
# Test block: calculates the average age
# -------------------------
if __name__ == "__main__":
    average_age()


