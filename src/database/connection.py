import psycopg2
import yaml

def db_connect():
    with open('C:/Users/Josh Ellis/Documents/programming/projects/wagner-group-data-collection/config.yaml', 'r') as f:
        credentials = yaml.safe_load(f)
        
    port_id = credentials['PostgresCredentials']['PORT']

    connection = None
    cursor = None
    try:
        connection = psycopg2.connect(
            host=credentials['PostgresCredentials']['DB_HOST'],
            database=credentials['PostgresCredentials']['DB_NAME'],
            user=credentials['PostgresCredentials']['DB_USER'],
            password=credentials['PostgresCredentials']['DB_PASS'],
            port=port_id
        )
        cursor = connection.cursor()
    except Exception as error:
        print(error)
    
    return connection, cursor

