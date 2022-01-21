import inspect
import os

import mysql.connector

filePath = os.path.relpath(__file__)


class MYSQL:
    def __init__(self, config):
        self.config = config
        self.database = None

    def connect(self, connectionString):
        func = inspect.currentframe()
        try:
            url = connectionString["url"].split(":")
            self.database = mysql.connector.connect(host=url[0], port=int(url[1]), user=connectionString["username"],
                                                    password=connectionString["password"],
                                                    database=connectionString["database"],
                                                    connection_timeout=self.config.dbDetails.mySQL["timeout"])
            self.config.log.info(filePath, func, "Database [{}] connected successfully..".format(connectionString["database"]))
            return self.database, None
        except Exception as e:
            self.config.log.error(filePath, func, "Error connecting mySQL Database [{}] => {}".format(connectionString["database"], e))
            return None, e

    def execute(self, query):
        func = inspect.currentframe()
        try:
            cursor = self.database.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            return result, None
        except Exception as e:
            self.config.log.error(filePath, func, "Error Fetching data from mySQL: {}".format(e))
            return None, e
