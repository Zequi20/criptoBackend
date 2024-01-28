import mysql.connector

db_config = {
    'user': 'zequi',
    'password': 'Zequi!-2000',
    'host': 'localhost',
    'database': 'coin',
    'autocommit': True
}

conn = mysql.connector.connect(**db_config)