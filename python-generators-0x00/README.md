# ALX Python Generators 

## Seed Database

This project sets up a MySQL database (`ALX_prodev`) and a table (`user_data`) for streaming user data using Python generators.

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
