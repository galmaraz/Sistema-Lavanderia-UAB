import mysql.connector
from flask import g, current_app
from mysql.connector import Error

def connect_db():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",  # Cambia por tu usuario
            password="uab-2025",  # Usa la que configuraste
            database="db_lavanderia",
            auth_plugin='mysql_native_password'  # Necesario para MySQL 8+
        )
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        raise

def get_db():
    if 'db' not in g:
        g.db = connect_db()
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()