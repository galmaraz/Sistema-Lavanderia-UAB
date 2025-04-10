from app.db import get_db
import re

def validar_datos_usuario(nombre, correo, contrasena, tipo_usuario):
    """Valida los datos del usuario antes de insertar en la DB"""
    if not nombre or not correo or not contrasena or not tipo_usuario:
        return False, "Todos los campos son obligatorios"
    
    if not re.match(r'^[a-zA-Z0-9._%+-]+@uab\.edu\.bo$', correo):
        return False, "Solo se permiten correos institucionales @uab.edu.bo"
    
    if not re.match(r'^(?=.*[A-Z])(?=.*\d).{8,}$', contrasena):
        return False, "La contraseña debe tener al menos 8 caracteres, una mayúscula y un número"
    
    return True, ""

def usuario_existe(correo):
    """Verifica si un usuario ya existe en la base de datos"""
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id FROM usuarios WHERE correo = %s", (correo,))
        return cursor.fetchone() is not None
    finally:
        cursor.close()

def crear_usuario_en_db(nombre, correo, contrasena, tipo_usuario):
    """Crea un nuevo usuario en la base de datos"""
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO usuarios (nombre, correo, contrasena, tipo_usuario) VALUES (%s, %s, %s, %s)",
            (nombre, correo, contrasena, tipo_usuario)
        )
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()

def obtener_usuario_por_correo(correo):
    """Obtiene un usuario por su correo electrónico"""
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM usuarios WHERE correo = %s", (correo,))
        return cursor.fetchone()
    finally:
        cursor.close()