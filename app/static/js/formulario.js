// Ejemplo de manejo para evitar 'undefined' en `getWithTTL`

document.addEventListener('DOMContentLoaded', function () {
    // Suponiendo que el objeto `storage` es lo que tiene el método getWithTTL
    let storage;

    // Asegurarse de que 'storage' no sea undefined
    if (typeof storage !== 'undefined' && storage && typeof storage.getWithTTL === 'function') {
        // Si storage y getWithTTL existen, podemos llamar al método de forma segura
        const prompt = storage.getWithTTL('someKey');
        console.log(prompt);
    } else {
        console.error("El objeto 'storage' o su método 'getWithTTL' no están definidos correctamente.");
    }

    const formulario = document.getElementById('formulario');
    const errorCorreo = document.getElementById('error-correo');
    const errorContrasena = document.getElementById('error-contrasena');
    const mensaje = document.getElementById('mensaje');

    formulario.addEventListener('submit', async function (e) {
        e.preventDefault();

        // Limpiar mensajes de error previos
        errorCorreo.classList.add('hidden');
        errorContrasena.classList.add('hidden');
        mensaje.classList.add('hidden');
        
        // Obtener valores del formulario
        const nombre = document.getElementById('nombre').value.trim();
        const correo = document.getElementById('correo').value.trim();
        const contrasena = document.getElementById('contrasena').value.trim();
        const tipo_usuario = document.getElementById('tipo_usuario').value;

        // Validaciones
        if (!correo.endsWith('@uab.edu.bo')) {
            errorCorreo.textContent = "Solo se permiten correos institucionales @uab.edu.bo";
            errorCorreo.classList.remove('hidden');
            return;
        }
        
        if (contrasena.length < 8) {
            errorContrasena.textContent = "La contraseña debe tener al menos 8 caracteres";
            errorContrasena.classList.remove('hidden');
            return;
        }

        // Crear objeto con los datos del formulario
        const data = {
            nombre: nombre,
            correo: correo,
            contrasena: contrasena,
            tipo_usuario: tipo_usuario
        };

        // Enviar los datos al backend usando Fetch
        try {
            const response = await fetch('/usuarios', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            // Si la respuesta es exitosa (código 200-299)
            if (response.ok) {
                // Mostrar mensaje de éxito
                mensaje.textContent = result.mensaje || "Usuario creado exitosamente.";
                mensaje.classList.remove('hidden', 'text-red-500');
                mensaje.classList.add('text-green-500');
                formulario.reset();

                // Redirigir a la página de login después de 2 segundos
                setTimeout(function() {
                    window.location.href = '/';  // Redirige al login
                }, 2000);  // 2 segundos de espera antes de redirigir

            } else {
                // Mostrar mensaje de error (si no es exitoso)
                mensaje.textContent = result.error || "Hubo un error al procesar el formulario.";
                mensaje.classList.remove('hidden', 'text-green-500');
                mensaje.classList.add('text-red-500');
            }

        } catch (error) {
            console.error(error);
            mensaje.textContent = "Error al conectar con el servidor.";
            mensaje.classList.remove('hidden', 'text-green-500');
            mensaje.classList.add('text-red-500');
        }
    });
});
