document.addEventListener('DOMContentLoaded', function() {
    cargarInformacionUsuario();
});

async function cargarInformacionUsuario() {
    try {
        const response = await fetch('/get_user_info');
        const result = await response.json();
        
        if (result.success) {
            document.getElementById('userName').textContent = result.nombre;
            document.getElementById('userEmail').textContent = result.email;
            document.getElementById('userRol').textContent = result.rol;
        } else {
            console.error('Error al cargar información del usuario');
        }
    } catch (error) {
        console.error('Error:', error);
    }
}
