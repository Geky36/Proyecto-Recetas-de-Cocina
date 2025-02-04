import mysql.connector

db_config = {
    'user': 'dilan',
    'password': '123456',
    'host': 'localhost',
    'database': 'Hospital',
    'raise_on_warnings': True
}

def get_db_connection():
    return mysql.connector.connect(**db_config)
