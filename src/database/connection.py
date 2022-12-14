import psycopg2
import os

def db_connect():
    connection = None
    cursor = None
    
    try:
        connection = psycopg2.connect(
            host=os.getenv('localhost'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASS'),
            port=5432
        )
        cursor = connection.cursor()
    except Exception as error:
        print(error)
    
    return connection, cursor

