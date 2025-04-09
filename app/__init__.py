from flask import Flask
import os

# Crear la aplicación Flask con rutas explícitas
app = Flask(__name__, 
            template_folder=os.path.join(os.path.dirname(__file__), 'templates'),
            static_folder=os.path.join(os.path.dirname(__file__), 'static'))

# Configurar el secreto para las sesiones (clave secreta para firmar las cookies de sesión)
app.config['SECRET_KEY'] = 'clave_secreta'

# Configuración de la base de datos MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'uab-2025'
app.config['MYSQL_DB'] = 'db_lavanderia'

# Configuración de la sesión
app.config['SESSION_COOKIE_NAME'] = 'session_id'  # Nombre de la cookie de sesión
app.config['SESSION_TYPE'] = 'filesystem'  # Puedes elegir entre 'filesystem' o 'redis'
app.config['SESSION_PERMANENT'] = False  # Define si la sesión debe durar más allá de la sesión del navegador

# Configurar base de datos
from app.db import get_db, close_db
app.teardown_appcontext(close_db)

# Importar rutas DESPUÉS de crear la app
from app.routes import *
