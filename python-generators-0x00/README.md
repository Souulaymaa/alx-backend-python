# ALX Python Generators 

## Seed Database

This project demonstrates how to set up a MySQL database, populate it with sample data, and stream rows using Python generators.

### Overview

We created a `seed.py` script that:

1. **Connects to MySQL**  
   - Uses a dedicated user `alx_user` with password `leetcode`.

2. **Creates the database**  
   - `ALX_prodev` is created if it doesn’t already exist.

3. **Creates the table**  
   - `user_data` table includes fields:  
     `user_id` (UUID, Primary Key), `name`, `email`, `age`.

4. **Inserts sample data**  
   - Populates the table with sample users directly in Python (no CSV required).

5. **Prepared for generator use**  
   - Data is now ready to be streamed row by row using a generator.

### How to Run

1. Make sure MySQL is running on your machine.
2. Run the seed script:

```bash
python3 seed.py
```
You should see:

```bash
Connected to MySQL server
Table user_data created successfully
Sample data inserted successfully
Seeded database successfully
```

The `user_data` table is now ready for your Python generators.

### Notes
- The script uses the MySQL user `alx_user` with password `leetcode`.
- You can change these in `seed.py` if you prefer a different user/password.
- No CSV file is required; sample data is hardcoded into the script.

## Stream Rows from an SQL Database

### Overview
The `0-stream_users.py` script:
- Defines a generator function `stream_users()` that fetches rows from the `user_data` table **one by one**.
- Converts `age` from Decimal to integer.
- Can be used in other scripts to iterate over rows lazily without loading all data at once.

### Test the generator directly:
```bash
python3 0-stream_users.py
```

You should see: Output (first 6 rows):
```python
{'user_id': '...', 'name': 'Dan Altenwerth Jr.', 'email': 'Molly59@gmail.com', 'age': 67}
{'user_id': '...', 'name': 'Glenda Wisozk', 'email': 'Miriam21@gmail.com', 'age': 119}
...
```

## Batch Processing

### Overview
The `1-batch_processing.py` script (has):
- Generator function `stream_users_in_batches(batch_size)` that fetches rows **in batches** from the database.  
- Generator function `batch_processing(batch_size)` that **filters users over 25** from each batch.  
- Explicitly unpacks dictionary fields to avoid editor/type warnings.

### Test the batch processing
```bash
python3 0-batch_users.py
```

You should see: Output (first 6 users over age 25):
```python
{'user_id': '...', 'name': 'Dan Altenwerth Jr.', 'email': 'Molly59@gmail.com', 'age': 67}
{'user_id': '...', 'name': 'Glenda Wisozk', 'email': 'Miriam21@gmail.com', 'age': 119}
...
```