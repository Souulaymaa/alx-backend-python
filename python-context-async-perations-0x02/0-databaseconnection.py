import sqlite3

class DatabaseConnection:
    def __init__(self, db_name):
        #initialize the object
        self.db_name = db_name
        self.connection = None
    
    def __enter__(self):
        #open the conection
        self.connection = sqlite3.connect(self.db_name)
        return self.connection

    def __exit__(self, exc_type, exc_value, exc_traceback):
        #close the connection
        if self.connection:
            self.connection.close()

if __name__ == "__main__":
        with DatabaseConnection('users.db') as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM users;")
            # fetchall() returns a list of tuples, where each tuple represents a row from the table.
            results = cursor.fetchall()
            print(results)
