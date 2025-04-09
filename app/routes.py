from flask import render_template, request, jsonify, redirect, flash, url_for, session
from app import app
from app.db import get_db
from werkzeug.security import generate_password_hash, check_password_hash  # Para manejar contraseñas seguras

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'usuario_id' in session:
        return redirect('/dashboard')  # Si ya está logueado, redirige al dashboard
    
    if request.method == 'POST':
        correo = request.form['correo']
        contrasena = request.form['contrasena']

        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE correo = %s", (correo,))
        usuario = cursor.fetchone()

        if usuario and check_password_hash(usuario['contrasena'], contrasena):  # Verifica la contraseña hasheada
            # Si las credenciales son correctas, redirigimos a la página principal
            session['usuario_id'] = usuario['id']  # Guardamos el id del usuario en la sesión
            flash('Inicio de sesión exitoso', 'success')
            return redirect('/dashboard')  # Página protegida con la sesión
        else:
            flash('Correo o contraseña incorrectos', 'error')
            return render_template('login.html')

    # Si es GET, simplemente renderiza el login
    return render_template('login.html')


@app.route('/usuarios', methods=['GET','POST'])
def crear_usuario():
    # Obtener los datos del formulario, que vienen como JSON
    data = request.get_json()
    nombre = data.get('nombre')
    correo = data.get('correo')
    contrasena = data.get('contrasena')
    tipo_usuario = data.get('tipo_usuario')

    # Validaciones
    if not nombre or not correo or not contrasena or not tipo_usuario:
        return jsonify({'error': 'Todos los campos son obligatorios'}), 400

    # Validar el correo institucional
    if not correo.endswith('@uab.edu.bo'):
        return jsonify({'error': 'El correo debe ser institucional (@uab.edu.bo)'}), 400

    # Verificar si el correo ya está registrado
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE correo = %s", (correo,))
    if cursor.fetchone():
        return jsonify({'error': 'El correo ya está registrado'}), 409

    # Hashear la contraseña antes de guardarla
    contrasena_hash = generate_password_hash(contrasena)

    # Guardar el nuevo usuario en la base de datos
    cursor.execute("INSERT INTO usuarios (nombre, correo, contrasena, tipo_usuario) VALUES (%s, %s, %s, %s)",
                   (nombre, correo, contrasena_hash, tipo_usuario))
    db.commit()

    return jsonify({'mensaje': 'Usuario creado exitosamente.'}), 201
