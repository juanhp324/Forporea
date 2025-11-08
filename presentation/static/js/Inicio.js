document.addEventListener('DOMContentLoaded', function() {
    cargarInformacionUsuario();
});

async function cargarInformacionUsuario() {
    try {
        const response = await fetch('/get_user_info');
        const result = await response.json();
        
        if (result.success) {
            document.getElementById('userName').textContent = result.nombre;
            document.getElementById('userEmail').textContent = result.user;
            document.getElementById('userRol').textContent = result.rol;
        }
    } catch (error) {
        // Error silencioso
    }
}
