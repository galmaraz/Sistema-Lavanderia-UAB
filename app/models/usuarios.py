# models/usuario.py
import bcrypt
from app.db import get_db

class Usuario:
    def __init__(self, nombre, correo, contrasena, tipo_usuario):
        self.nombre = nombre
        self.correo = correo
        self.contrasena = contrasena
        self.tipo_usuario = tipo_usuario

    # Método para guardar el usuario en la base de datos
    def guardar(self):
        db = get_db()
        cursor = db.cursor(dictionary=True)

        # Hashear la contraseña
        hashed_password = bcrypt.hashpw(self.contrasena.encode('utf-8'), bcrypt.gensalt())

        try:
            cursor.execute("""
                INSERT INTO usuarios (nombre, correo, contrasena, tipo_usuario)
                VALUES (%s, %s, %s, %s)
            """, (self.nombre, self.correo, hashed_password.decode('utf-8'), self.tipo_usuario))
            db.commit()
            cursor.close()
            return True
        except Exception as e:
            db.rollback()
            cursor.close()
            print(f"Error al guardar el usuario: {e}")
            return False

    # Método para verificar si un correo ya está registrado
    @staticmethod
    def existe(correo):
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE correo = %s", (correo,))
        usuario = cursor.fetchone()
        cursor.close()
        return usuario is not None
