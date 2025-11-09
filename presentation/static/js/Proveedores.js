let proveedores = [];
let modoEdicion = false;
let proveedorIdEditar = null;
let permisos = {};

document.addEventListener('DOMContentLoaded', async function() {
    await cargarPermisos();
    await cargarProveedores();
});

async function cargarPermisos() {
    try {
        const response = await fetch('/get_user_info');
        const result = await response.json();
        if (result.success) {
            permisos = result.permisos.proveedores || [];
            
            // Actualizar versión en el navbar
            if (result.version && result.version.version) {
                const versionElement = document.getElementById('appVersion');
                if (versionElement) {
                    versionElement.textContent = 'v' + result.version.version;
                }
            }
        }
    } catch (error) {
        console.error('Error al cargar permisos:', error);
    }
}

async function cargarProveedores() {
    const tbody = document.getElementById('tablaProveedores');
    tbody.innerHTML = '<tr><td colspan="6" class="text-center"><div class="spinner-border text-primary" role="status"><span class="visually-hidden">Cargando...</span></div></td></tr>';
    
    try {
        const response = await fetch('/get_proveedores');
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        
        if (result.success) {
            proveedores = result.proveedores;
            mostrarProveedores();
        } else {
            throw new Error(result.message || 'Error desconocido');
        }
    } catch (error) {
        console.error('Error al cargar proveedores:', error);
        tbody.innerHTML = '<tr><td colspan="6" class="text-center text-danger">Error al cargar proveedores. <button class="btn btn-sm btn-primary ms-2" onclick="cargarProveedores()">Reintentar</button></td></tr>';
        mostrarMensaje('Error al cargar proveedores. Por favor, intenta de nuevo.', 'error');
    }
}

function mostrarProveedores() {
    const tbody = document.getElementById('tablaProveedores');
    
    if (proveedores.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" class="text-center">No hay proveedores registrados</td></tr>';
        return;
    }
    
    const puedeEditar = permisos.includes('editar');
    const puedeEliminar = permisos.includes('eliminar');
    
    tbody.innerHTML = proveedores.map(proveedor => `
        <tr>
            <td>${proveedor.nombre}</td>
            <td>${proveedor.contacto}</td>
            <td>${proveedor.telefono || 'N/A'}</td>
            <td>${proveedor.email || 'N/A'}</td>
            <td>${proveedor.direccion || 'N/A'}</td>
            <td>
                <button class="btn btn-info btn-sm" onclick="verDetalleProveedor('${proveedor._id}')">
                    <i class="fas fa-eye"></i>
                </button>
                ${puedeEditar ? `
                <button class="btn btn-warning btn-sm" onclick="editarProveedor('${proveedor._id}')">
                    <i class="fas fa-edit"></i>
                </button>
                ` : ''}
                ${puedeEliminar ? `
                <button class="btn btn-danger btn-sm" onclick="eliminarProveedor('${proveedor._id}')">
                    <i class="fas fa-trash"></i>
                </button>
                ` : ''}
            </td>
        </tr>
    `).join('');
    
    // Ocultar botón de nuevo proveedor si no tiene permiso de crear
    const btnNuevo = document.querySelector('[data-bs-target="#modalProveedor"]');
    if (btnNuevo && !permisos.includes('crear')) {
        btnNuevo.style.display = 'none';
    }
}

function abrirModalNuevo() {
    modoEdicion = false;
    proveedorIdEditar = null;
    document.getElementById('modalProveedorTitle').textContent = 'Nuevo Proveedor';
    document.getElementById('formProveedor').reset();
    document.getElementById('proveedorId').value = '';
}

function editarProveedor(id) {
    modoEdicion = true;
    proveedorIdEditar = id;
    
    const proveedor = proveedores.find(p => p._id === id);
    if (!proveedor) return;
    
    document.getElementById('modalProveedorTitle').textContent = 'Editar Proveedor';
    document.getElementById('proveedorId').value = id;
    document.getElementById('proveedorNombre').value = proveedor.nombre;
    document.getElementById('proveedorContacto').value = proveedor.contacto;
    document.getElementById('proveedorTelefono').value = proveedor.telefono || '';
    document.getElementById('proveedorEmail').value = proveedor.email || '';
    document.getElementById('proveedorDireccion').value = proveedor.direccion || '';
    
    const modal = new bootstrap.Modal(document.getElementById('modalProveedor'));
    modal.show();
}

async function guardarProveedor() {
    const nombre = document.getElementById('proveedorNombre').value;
    const contacto = document.getElementById('proveedorContacto').value;
    const telefono = document.getElementById('proveedorTelefono').value;
    const email = document.getElementById('proveedorEmail').value;
    const direccion = document.getElementById('proveedorDireccion').value;
    
    if (!nombre || !contacto) {
        mostrarMensaje('Por favor completa todos los campos obligatorios', 'warning');
        return;
    }
    
    const data = {
        nombre,
        contacto,
        telefono,
        email,
        direccion
    };
    
    try {
        let response;
        if (modoEdicion) {
            response = await fetch(`/update_proveedor/${proveedorIdEditar}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
        } else {
            response = await fetch('/create_proveedor', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
        }
        
        const result = await response.json();
        
        if (result.success) {
            mostrarMensaje(result.message, 'success');
            bootstrap.Modal.getInstance(document.getElementById('modalProveedor')).hide();
            cargarProveedores();
        } else {
            mostrarMensaje(result.message, 'error');
        }
    } catch (error) {
        mostrarMensaje('Error al guardar proveedor', 'error');
    }
}

async function eliminarProveedor(id) {
    const confirmed = await showConfirm({
        title: 'Eliminar Proveedor',
        message: '¿Estás seguro de que deseas eliminar este proveedor? Esta acción no se puede deshacer y puede afectar los productos asociados.',
        confirmText: 'Sí, eliminar',
        cancelText: 'Cancelar',
        type: 'danger',
        icon: 'fas fa-trash-alt'
    });
    
    if (!confirmed) return;
    
    try {
        const response = await fetch(`/delete_proveedor/${id}`, {
            method: 'DELETE'
        });
        
        const result = await response.json();
        
        if (result.success) {
            mostrarMensaje(result.message, 'success');
            cargarProveedores();
        } else {
            mostrarMensaje(result.message, 'error');
        }
    } catch (error) {
        mostrarMensaje('Error al eliminar proveedor', 'error');
    }
}

async function verDetalleProveedor(id) {
    try {
        const response = await fetch(`/get_proveedor/${id}`);
        const result = await response.json();
        
        if (result.success) {
            const proveedor = result.proveedor;
            
            document.getElementById('detalleProvNombre').textContent = proveedor.nombre;
            document.getElementById('detalleProvContacto').textContent = proveedor.contacto;
            document.getElementById('detalleProvTelefono').textContent = proveedor.telefono || 'N/A';
            document.getElementById('detalleProvEmail').textContent = proveedor.email || 'N/A';
            document.getElementById('detalleProvDireccion').textContent = proveedor.direccion || 'N/A';
            
            const modal = new bootstrap.Modal(document.getElementById('modalDetalleProveedor'));
            modal.show();
        }
    } catch (error) {
        mostrarMensaje('Error al cargar detalle del proveedor', 'error');
    }
}

function mostrarMensaje(mensaje, tipo) {
    showNotification(mensaje, tipo);
}
