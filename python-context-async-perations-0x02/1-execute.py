import sqlite3

class ExecuteQuery:

    def __init__(self, query, parameter, db_name):
        self.db_name = db_name
        self.connection = None
        self.query = query
        self.parameter = parameter if isinstance(parameter, tuple) else (parameter,)
        self.cursor = None

    def __enter__(self):
        #open the conection
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        self.cursor.execute(self.query, self.parameter)
        return self.cursor.fetchall()


    def __exit__(self, exc_type, exc_value, exc_traceback):
         #close the connection
        if self.connection:
            self.connection.close()

if __name__ == "__main__":
     query = ("SELECT * FROM users WHERE age > ?")
     parameter = 25
     with ExecuteQuery(query, parameter, 'users.db') as results:
            print(results)