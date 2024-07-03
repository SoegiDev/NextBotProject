import mysql.connector
from dotenv import load_dotenv
import os

database = []


def createDatabase():
    check_list_database = DBinit.checkDatabase()
    db_name = os.getenv("DB_NAME")
    if db_name not in check_list_database:
        mydb = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        my_cursor = mydb.cursor()
        my_cursor.execute(f"CREATE DATABASE {db_name}")
    check = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
    )
    return check.is_connected()


class DBinit:

    @staticmethod
    def checkDatabase():
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password=""
        )
        my_cursor = mydb.cursor()

        my_cursor.execute("show databases")

        my_result = my_cursor.fetchall()
        for x in my_result:
            database.append(x[0])
        return database
