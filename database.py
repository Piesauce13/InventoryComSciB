import mysql.connector
db_name = "storeDB"

class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="rootpassword",
            database= db_name
        )