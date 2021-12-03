import mysql.connector

class MYSQL:
    def __init__(self):
        pass
    def connect(self,connectionString):
        self.mydb = mysql.connector.connect(
            host=connectionString.host,
            user=connectionString.username,
            password=connectionString.password
        )
    def execute(self,query):
        cursor = self.mydb.cursor()
        cursor.execute("SELECT * FROM customers")
        result = cursor.fetchall()


