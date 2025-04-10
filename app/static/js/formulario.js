document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('formulario');
    const mensaje = document.getElementById('mensaje');
    const correoInput = document.getElementById('correo');
    const contrasenaInput = document.getElementById('contrasena');

    // Validación en tiempo real
    correoInput.addEventListener('input', validarCorreo);
    contrasenaInput.addEventListener('input', validarContrasena);

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const nombre = document.getElementById('nombre').value.trim();
        const correo = correoInput.value.trim();
        const contrasena = contrasenaInput.value;
        const tipo_usuario = document.getElementById('tipo_usuario').value;

        // Validación frontend
        if (!validarFormulario()) {
            return;
        }

        const datos = { 
            nombre, 
            correo, 
            contrasena, 
            tipo_usuario 
        };

        try {
            const response = await fetch('api/usuarios', {  // ← Ruta exacta
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({
                    nombre: nombre,
                    correo: correo,
                    contrasena: contrasena,
                    tipo_usuario: tipo_usuario
                })
            });
        
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.message || 'Error del servidor');
            }
        
            const data = await response.json();
            console.log('Éxito:', data);
        } catch (error) {
            console.error('Error:', error);
        }
    });

    function validarFormulario() {
        let isValid = true;
        
        // Validar nombre
        const nombre = document.getElementById('nombre').value.trim();
        if (!nombre) {
            mostrarError('nombre-error', 'El nombre es requerido');
            isValid = false;
        } else {
            ocultarError('nombre-error');
        }
        
        // Validar correo
        if (!validarCorreo()) {
            isValid = false;
        }
        
        // Validar contraseña
        if (!validarContrasena()) {
            isValid = false;
        }
        
        // Validar tipo de usuario
        const tipoUsuario = document.getElementById('tipo_usuario').value;
        if (!tipoUsuario) {
            mostrarError('tipo-error', 'Seleccione un tipo de usuario');
            isValid = false;
        } else {
            ocultarError('tipo-error');
        }
        
        return isValid;
    }
    
    function validarCorreo() {
        const correo = correoInput.value.trim();
        const correoPattern = /^[a-zA-Z0-9._%+-]+@uab\.edu\.bo$/;
        
        if (!correo) {
            mostrarError('correo-error', 'El correo es requerido');
            return false;
        }
        
        if (!correoPattern.test(correo)) {
            mostrarError('correo-error', 'Solo se permiten correos institucionales @uab.edu.bo');
            return false;
        }
        
        ocultarError('correo-error');
        return true;
    }
    
    function validarContrasena() {
        const contrasena = contrasenaInput.value;
        const contrasenaPattern = /^(?=.*[A-Z])(?=.*\d).{8,}$/;
        
        if (!contrasena) {
            mostrarError('contrasena-error', 'La contraseña es requerida');
            return false;
        }
        
        if (!contrasenaPattern.test(contrasena)) {
            mostrarError('contrasena-error', 'La contraseña debe tener al menos 8 caracteres, una mayúscula y un número');
            return false;
        }
        
        ocultarError('contrasena-error');
        return true;
    }
    
    function mostrarError(elementId, message) {
        const element = document.getElementById(elementId);
        element.textContent = message;
        element.classList.remove('hidden');
    }

    function ocultarError(elementId) {
        const element = document.getElementById(elementId);
        element.classList.add('hidden');
    }

    function mostrarMensaje(texto, tipo) {
        mensaje.textContent = texto;
        mensaje.className = tipo === 'exito' ? 'text-green-600' : 'text-red-600';
        mensaje.classList.remove('hidden');
        
        // Ocultar después de 5 segundos
        setTimeout(() => {
            mensaje.classList.add('hidden');
        }, 5000);
    }
});