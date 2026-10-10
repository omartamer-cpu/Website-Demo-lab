import os
import pymysql
from dotenv import load_dotenv

load_dotenv()

connection = pymysql.connect(
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT", "3306")),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
)

try:
    with connection.cursor() as cursor:
        cursor.execute("SHOW TABLES")
        print("Connected successfully!")

        for table in cursor.fetchall():
            print(table[0])
finally:
    connection.close()