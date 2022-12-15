import psycopg2
import os
from dotenv import dotenv_values


def db_connect():
    config = dotenv_values('.env')
    connection = None
    cursor = None
    
    try:
        connection = psycopg2.connect(
            host=config.get('localhost'),
            database=config.get('DB_NAME'),
            user=config.get('DB_USER'),
            password=config.get('DB_PASS'),
            port=5432
        )
        cursor = connection.cursor()
    except Exception as error:
        print(error)
    
    return connection, cursor

