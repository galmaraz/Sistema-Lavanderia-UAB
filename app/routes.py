from flask import render_template, request, jsonify, redirect, flash, session, current_app
from app import app, bcrypt
from app.models.usuarios import (
    validar_datos_usuario,
    usuario_existe,
    crear_usuario_en_db,
    obtener_usuario_por_correo
)
from werkzeug.security import check_password_hash, generate_password_hash
import re

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'usuario_id' in session:
        return redirect('/dashboard')
    
    if request.method == 'POST':
        correo = request.form['correo']
        contrasena = request.form['contrasena']

        usuario = obtener_usuario_por_correo(correo)
        if usuario and check_password_hash(usuario['contrasena'], contrasena):
            session['usuario_id'] = usuario['id']
            flash('Inicio de sesión exitoso', 'success')
            return redirect('/dashboard')
        else:
            flash('Correo o contraseña incorrectos', 'error')
    
    return render_template('login.html')

@app.route('/api/usuarios', methods=['POST'])
def api_registrar_usuario():
    data = request.get_json()
    
    try:
        # Validaciones
        required_fields = ['nombre', 'correo', 'contrasena', 'tipo_usuario']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Todos los campos son requeridos'}), 400

        if not re.match(r'^[a-zA-Z0-9._%+-]+@uab\.edu\.bo$', data['correo']):
            return jsonify({'error': 'Solo se permiten correos institucionales @uab.edu.bo'}), 400

        if not re.match(r'^(?=.*[A-Z])(?=.*\d).{8,}$', data['contrasena']):
            return jsonify({'error': 'La contraseña debe tener al menos 8 caracteres, una mayúscula y un número'}), 400

        if usuario_existe(data['correo']):
            return jsonify({'error': 'El correo electrónico ya está registrado'}), 409

        # Hash de la contraseña
        hashed_pwd = generate_password_hash(data['contrasena'])

        # Crear usuario
        user_id = crear_usuario_en_db(
            data['nombre'],
            data['correo'],
            hashed_pwd,
            data['tipo_usuario']
        )

        return jsonify({
            'message': 'Usuario registrado exitosamente',
            'usuario_id': user_id
        }), 201

    except Exception as e:
        current_app.logger.error(f'Error en API registro: {str(e)}')
        return jsonify({'error': 'Error al registrar el usuario'}), 500

@app.route('/dashboard')
def dashboard():
    if 'usuario_id' not in session:
        return redirect('/')
    return render_template('dashboard.html')