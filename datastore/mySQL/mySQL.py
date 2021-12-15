import mysql.connector


class MYSQL:
    def __init__(self):
        self.mydb = ""


    def connect(self, connectionString):
        url = connectionString["url"].split(":")
        self.mydb = mysql.connector.connect(host=url[0], port=int(url[1]), user=connectionString["username"],
                                            password=connectionString["password"], database=connectionString["database"])
        return self.mydb

    def execute(self, query):
        cursor = self.mydb.cursor()
        cursor.execute(query)  # "SELECT * FROM customers")
        result = cursor.fetchall()
        return result