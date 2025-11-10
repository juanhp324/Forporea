let proveedores = [];
let modoEdicion = false;
let proveedorIdEditar = null;
let permisos = {};
let proveedoresFiltrados = [];

document.addEventListener('DOMContentLoaded', async function() {
    await cargarPermisos();
    await cargarProveedores();
    configurarBusqueda();
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
    const mobileContainer = document.getElementById('tablaProveedoresMobile');
    
    if (proveedores.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" class="text-center">No hay proveedores registrados</td></tr>';
        mobileContainer.innerHTML = '<div class="text-center py-5"><p class="text-muted">No hay proveedores registrados</p></div>';
        return;
    }
    
    const puedeEditar = permisos.includes('editar');
    const puedeEliminar = permisos.includes('eliminar');
    
    // Versión Desktop (Tabla)
    tbody.innerHTML = proveedores.map(proveedor => `
        <tr>
            <td><strong>${proveedor.nombre}</strong></td>
            <td><span class="badge-contacto">${proveedor.contacto}</span></td>
            <td><span class="badge-telefono">${proveedor.telefono || 'N/A'}</span></td>
            <td><span class="badge-email">${proveedor.email || 'N/A'}</span></td>
            <td><span class="badge-direccion">${proveedor.direccion || 'N/A'}</span></td>
            <td class="text-center">
                <button class="btn-action-clean btn-info" onclick="verDetalleProveedor('${proveedor._id}')" title="Ver detalle">
                    <i class="fas fa-eye"></i>
                </button>
                ${puedeEditar ? `
                <button class="btn-action-clean btn-warning" onclick="editarProveedor('${proveedor._id}')" title="Editar">
                    <i class="fas fa-edit"></i>
                </button>
                ` : ''}
                ${puedeEliminar ? `
                <button class="btn-action-clean btn-danger" onclick="eliminarProveedor('${proveedor._id}')" title="Eliminar">
                    <i class="fas fa-trash"></i>
                </button>
                ` : ''}
            </td>
        </tr>
    `).join('');
    
    // Versión Móvil (Cards)
    mobileContainer.innerHTML = proveedores.map(proveedor => `
        <div class="mobile-card">
            <div class="mobile-card-header">
                <div class="mobile-card-title">${proveedor.nombre}</div>
                <span class="badge bg-success"><i class="fas fa-truck"></i></span>
            </div>
            <div class="mobile-card-body">
                <div class="mobile-card-row">
                    <span class="mobile-card-label"><i class="fas fa-user me-1"></i>Contacto</span>
                    <span class="mobile-card-value">${proveedor.contacto}</span>
                </div>
                <div class="mobile-card-row">
                    <span class="mobile-card-label"><i class="fas fa-phone me-1"></i>Teléfono</span>
                    <span class="mobile-card-value">${proveedor.telefono || 'N/A'}</span>
                </div>
                <div class="mobile-card-row">
                    <span class="mobile-card-label"><i class="fas fa-envelope me-1"></i>Email</span>
                    <span class="mobile-card-value">${proveedor.email || 'N/A'}</span>
                </div>
                <div class="mobile-card-row">
                    <span class="mobile-card-label"><i class="fas fa-map-marker-alt me-1"></i>Dirección</span>
                    <span class="mobile-card-value">${proveedor.direccion || 'N/A'}</span>
                </div>
            </div>
            <div class="mobile-card-actions">
                <button class="btn btn-sm btn-info" onclick="verDetalleProveedor('${proveedor._id}')">
                    <i class="fas fa-eye me-1"></i>Ver
                </button>
                ${puedeEditar ? `
                <button class="btn btn-sm btn-warning" onclick="editarProveedor('${proveedor._id}')">
                    <i class="fas fa-edit me-1"></i>Editar
                </button>
                ` : ''}
                ${puedeEliminar ? `
                <button class="btn btn-sm btn-danger" onclick="eliminarProveedor('${proveedor._id}')">
                    <i class="fas fa-trash me-1"></i>Eliminar
                </button>
                ` : ''}
            </div>
        </div>
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

// ============================================
// FUNCIONALIDAD DE BÚSQUEDA
// ============================================

function configurarBusqueda() {
    const inputNombre = document.getElementById('buscarProveedorNombre');
    const inputId = document.getElementById('buscarProveedorId');
    
    if (inputNombre) {
        inputNombre.addEventListener('input', function() {
            if (this.value.trim()) {
                document.getElementById('buscarProveedorId').value = '';
            }
            buscarProveedoresFunc();
        });
    }
    
    if (inputId) {
        inputId.addEventListener('input', function() {
            if (this.value.trim()) {
                document.getElementById('buscarProveedorNombre').value = '';
            }
            buscarProveedoresFunc();
        });
    }
}

function buscarProveedoresFunc() {
    const busquedaNombre = document.getElementById('buscarProveedorNombre').value.trim().toLowerCase();
    const busquedaId = document.getElementById('buscarProveedorId').value.trim().toLowerCase();
    
    if (!busquedaNombre && !busquedaId) {
        proveedoresFiltrados = proveedores;
        mostrarProveedoresFiltrados();
        return;
    }
    
    proveedoresFiltrados = proveedores.filter(proveedor => {
        if (busquedaNombre) {
            return proveedor.nombre.toLowerCase().includes(busquedaNombre);
        }
        if (busquedaId) {
            return proveedor._id.toLowerCase().includes(busquedaId);
        }
        return false;
    });
    
    mostrarProveedoresFiltrados();
}

function mostrarProveedoresFiltrados() {
    const tbody = document.getElementById('tablaProveedores');
    const proveedoresAMostrar = proveedoresFiltrados.length > 0 || 
                                document.getElementById('buscarProveedorNombre').value.trim() || 
                                document.getElementById('buscarProveedorId').value.trim() 
                                ? proveedoresFiltrados : proveedores;
    
    if (proveedoresAMostrar.length === 0) {
        const busquedaNombre = document.getElementById('buscarProveedorNombre').value.trim();
        const busquedaId = document.getElementById('buscarProveedorId').value.trim();
        
        if (busquedaNombre || busquedaId) {
            tbody.innerHTML = '<tr><td colspan="6" class="text-center py-4"><i class="fas fa-search fa-2x text-muted mb-2 d-block"></i><p class="text-muted">No se encontraron proveedores con ese criterio de búsqueda</p></td></tr>';
        } else {
            tbody.innerHTML = '<tr><td colspan="6" class="text-center">No hay proveedores registrados</td></tr>';
        }
        return;
    }
    
    const puedeEditar = permisos.includes('editar');
    const puedeEliminar = permisos.includes('eliminar');
    
    tbody.innerHTML = proveedoresAMostrar.map(proveedor => `
        <tr>
            <td><strong>${proveedor.nombre}</strong></td>
            <td><span class="badge-contacto">${proveedor.contacto}</span></td>
            <td><span class="badge-telefono">${proveedor.telefono || 'N/A'}</span></td>
            <td><span class="badge-email">${proveedor.email || 'N/A'}</span></td>
            <td><span class="badge-direccion">${proveedor.direccion || 'N/A'}</span></td>
            <td class="text-center">
                <button class="btn-action-clean btn-info" onclick="verDetalleProveedor('${proveedor._id}')" title="Ver detalle">
                    <i class="fas fa-eye"></i>
                </button>
                ${puedeEditar ? `
                <button class="btn-action-clean btn-warning" onclick="editarProveedor('${proveedor._id}')" title="Editar">
                    <i class="fas fa-edit"></i>
                </button>
                ` : ''}
                ${puedeEliminar ? `
                <button class="btn-action-clean btn-danger" onclick="eliminarProveedor('${proveedor._id}')" title="Eliminar">
                    <i class="fas fa-trash"></i>
                </button>
                ` : ''}
            </td>
        </tr>
    `).join('');
}

function limpiarBusquedaProveedor() {
    document.getElementById('buscarProveedorNombre').value = '';
    document.getElementById('buscarProveedorId').value = '';
    proveedoresFiltrados = proveedores;
    mostrarProveedores();
}
