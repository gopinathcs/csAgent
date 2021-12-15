import mysql.connector
import pandas as pd

mydb = mysql.connector.connect(host="localhost",  port=3306, database="csagent", user="lenin", password="Login!23")
query = "select * from projects"
result_dataFrame = pd.read_sql(query, mydb).to_parquet('myfile.parquet')

print(result_dataFrame)

import os
os.remove("myfile.parquet")