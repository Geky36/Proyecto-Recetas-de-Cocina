import mysql.connector

db_config = {
    'user': 'BaseNOLE',
    'password': 'proyectofinal',
    'host': 'localhost',
    'database': 'RecetarioDigital',
    'raise_on_warnings': True
}

def get_db_connection():
    return mysql.connector.connect(**db_config)
