let productos = [];
let proveedores = [];
let modoEdicion = false;
let productoIdEditar = null;
let permisos = {};
let productosFiltrados = [];

document.addEventListener('DOMContentLoaded', async function() {
    await cargarPermisos();
    await cargarProductos();
    await cargarProveedores();
    configurarBusqueda();
});

async function cargarPermisos() {
    try {
        const response = await fetch('/get_user_info');
        const result = await response.json();
        if (result.success) {
            permisos = result.permisos.productos || [];
            
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

async function cargarProductos() {
    const tbody = document.getElementById('tablaProductos');
    tbody.innerHTML = '<tr><td colspan="6" class="text-center"><div class="spinner-border text-primary" role="status"><span class="visually-hidden">Cargando...</span></div></td></tr>';
    
    try {
        const response = await fetch('/get_productos');
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        
        if (result.success) {
            productos = result.productos;
            mostrarProductos();
        } else {
            throw new Error(result.message || 'Error desconocido');
        }
    } catch (error) {
        console.error('Error al cargar productos:', error);
        tbody.innerHTML = '<tr><td colspan="6" class="text-center text-danger">Error al cargar productos. <button class="btn btn-sm btn-primary ms-2" onclick="cargarProductos()">Reintentar</button></td></tr>';
        mostrarMensaje('Error al cargar productos. Por favor, intenta de nuevo.', 'error');
    }
}

async function cargarProveedores() {
    try {
        const response = await fetch('/get_proveedores');
        const result = await response.json();
        
        if (result.success) {
            proveedores = result.proveedores;
            llenarSelectProveedores();
        }
    } catch (error) {
        // Error silencioso
    }
}

function llenarSelectProveedores() {
    const select = document.getElementById('productoProveedor');
    select.innerHTML = '<option value="">Seleccione un proveedor</option>';
    
    proveedores.forEach(proveedor => {
        const option = document.createElement('option');
        option.value = proveedor._id;
        option.textContent = proveedor.nombre;
        select.appendChild(option);
    });
}

function mostrarProductos() {
    const tbody = document.getElementById('tablaProductos');
    
    if (productos.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" class="text-center">No hay productos registrados</td></tr>';
        return;
    }
    
    const puedeEditar = permisos.includes('editar');
    const puedeEliminar = permisos.includes('eliminar');
    
    tbody.innerHTML = productos.map(producto => `
        <tr>
            <td><strong>${producto.nombre}</strong></td>
            <td>${producto.descripcion || 'N/A'}</td>
            <td><span class="badge-precio">$${producto.precio.toFixed(2)}/lb</span></td>
            <td><span class="badge-stock-display">${parseFloat(producto.stock).toFixed(2)} lbs</span></td>
            <td><span class="badge-proveedor">${producto.proveedor_nombre}</span></td>
            <td class="text-center">
                <button class="btn-action-clean btn-info" onclick="verDetalleProducto('${producto._id}')" title="Ver detalle">
                    <i class="fas fa-eye"></i>
                </button>
                ${puedeEditar ? `
                <button class="btn-action-clean btn-warning" onclick="editarProducto('${producto._id}')" title="Editar">
                    <i class="fas fa-edit"></i>
                </button>
                ` : ''}
                ${puedeEliminar ? `
                <button class="btn-action-clean btn-danger" onclick="eliminarProducto('${producto._id}')" title="Eliminar">
                    <i class="fas fa-trash"></i>
                </button>
                ` : ''}
            </td>
        </tr>
    `).join('');
    
    // Ocultar botón de nuevo producto si no tiene permiso de crear
    const btnNuevo = document.querySelector('[data-bs-target="#modalProducto"]');
    if (btnNuevo && !permisos.includes('crear')) {
        btnNuevo.style.display = 'none';
    }
}

function abrirModalNuevo() {
    modoEdicion = false;
    productoIdEditar = null;
    document.getElementById('modalProductoTitle').textContent = 'Nuevo Producto';
    document.getElementById('formProducto').reset();
    document.getElementById('productoId').value = '';
}

function editarProducto(id) {
    modoEdicion = true;
    productoIdEditar = id;
    
    const producto = productos.find(p => p._id === id);
    if (!producto) return;
    
    document.getElementById('modalProductoTitle').textContent = 'Editar Producto';
    document.getElementById('productoId').value = id;
    document.getElementById('productoNombre').value = producto.nombre;
    document.getElementById('productoDescripcion').value = producto.descripcion || '';
    document.getElementById('productoPrecio').value = producto.precio;
    document.getElementById('productoStock').value = producto.stock;
    document.getElementById('productoProveedor').value = producto.proveedor_id;
    
    const modal = new bootstrap.Modal(document.getElementById('modalProducto'));
    modal.show();
}

async function guardarProducto() {
    const nombre = document.getElementById('productoNombre').value;
    const descripcion = document.getElementById('productoDescripcion').value;
    const precio = document.getElementById('productoPrecio').value;
    const stock = document.getElementById('productoStock').value;
    const proveedor_id = document.getElementById('productoProveedor').value;
    
    if (!nombre || !precio || !stock || !proveedor_id) {
        mostrarMensaje('Por favor completa todos los campos obligatorios', 'warning');
        return;
    }
    
    const data = {
        nombre,
        descripcion,
        precio: parseFloat(precio),
        stock: parseFloat(stock),
        proveedor_id
    };
    
    try {
        let response;
        if (modoEdicion) {
            response = await fetch(`/update_producto/${productoIdEditar}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
        } else {
            response = await fetch('/create_producto', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
        }
        
        const result = await response.json();
        
        if (result.success) {
            mostrarMensaje(result.message, 'success');
            bootstrap.Modal.getInstance(document.getElementById('modalProducto')).hide();
            cargarProductos();
        } else {
            mostrarMensaje(result.message, 'error');
        }
    } catch (error) {
        mostrarMensaje('Error al guardar producto', 'error');
    }
}

async function eliminarProducto(id) {
    const confirmed = await showConfirm({
        title: 'Eliminar Producto',
        message: '¿Estás seguro de que deseas eliminar este producto? Esta acción no se puede deshacer.',
        confirmText: 'Sí, eliminar',
        cancelText: 'Cancelar',
        type: 'danger',
        icon: 'fas fa-trash-alt'
    });
    
    if (!confirmed) return;
    
    try {
        const response = await fetch(`/delete_producto/${id}`, {
            method: 'DELETE'
        });
        
        const result = await response.json();
        
        if (result.success) {
            mostrarMensaje(result.message, 'success');
            cargarProductos();
        } else {
            mostrarMensaje(result.message, 'error');
        }
    } catch (error) {
        mostrarMensaje('Error al eliminar producto', 'error');
    }
}

async function verDetalleProducto(id) {
    try {
        const response = await fetch(`/get_producto/${id}`);
        const result = await response.json();
        
        if (result.success) {
            const producto = result.producto;
            document.getElementById('detalleNombre').textContent = producto.nombre;
            document.getElementById('detalleDescripcion').textContent = producto.descripcion || 'N/A';
            document.getElementById('detallePrecio').textContent = producto.precio.toFixed(2);
            document.getElementById('detalleStock').textContent = parseFloat(producto.stock).toFixed(2);
            
            document.getElementById('detalleProveedorNombre').textContent = producto.proveedor.nombre;
            document.getElementById('detalleProveedorContacto').textContent = producto.proveedor.contacto || 'N/A';
            document.getElementById('detalleProveedorTelefono').textContent = producto.proveedor.telefono || 'N/A';
            document.getElementById('detalleProveedorEmail').textContent = producto.proveedor.email || 'N/A';
            document.getElementById('detalleProveedorDireccion').textContent = producto.proveedor.direccion || 'N/A';
            
            const modal = new bootstrap.Modal(document.getElementById('modalDetalleProducto'));
            modal.show();
        }
    } catch (error) {
        mostrarMensaje('Error al cargar detalle del producto', 'error');
    }
}

function mostrarMensaje(mensaje, tipo) {
    showNotification(mensaje, tipo);
}

// ============================================
// FUNCIONALIDAD DE BÚSQUEDA
// ============================================

function configurarBusqueda() {
    const inputNombre = document.getElementById('buscarProductoNombre');
    const inputId = document.getElementById('buscarProductoId');
    
    if (inputNombre) {
        inputNombre.addEventListener('input', function() {
            if (this.value.trim()) {
                document.getElementById('buscarProductoId').value = '';
            }
            buscarProductos();
        });
    }
    
    if (inputId) {
        inputId.addEventListener('input', function() {
            if (this.value.trim()) {
                document.getElementById('buscarProductoNombre').value = '';
            }
            buscarProductos();
        });
    }
}

function buscarProductos() {
    const busquedaNombre = document.getElementById('buscarProductoNombre').value.trim().toLowerCase();
    const busquedaId = document.getElementById('buscarProductoId').value.trim().toLowerCase();
    
    if (!busquedaNombre && !busquedaId) {
        productosFiltrados = productos;
        mostrarProductosFiltrados();
        return;
    }
    
    productosFiltrados = productos.filter(producto => {
        if (busquedaNombre) {
            return producto.nombre.toLowerCase().includes(busquedaNombre);
        }
        if (busquedaId) {
            return producto._id.toLowerCase().includes(busquedaId);
        }
        return false;
    });
    
    mostrarProductosFiltrados();
}

function mostrarProductosFiltrados() {
    const tbody = document.getElementById('tablaProductos');
    const productosAMostrar = productosFiltrados.length > 0 || 
                              document.getElementById('buscarProductoNombre').value.trim() || 
                              document.getElementById('buscarProductoId').value.trim() 
                              ? productosFiltrados : productos;
    
    if (productosAMostrar.length === 0) {
        const busquedaNombre = document.getElementById('buscarProductoNombre').value.trim();
        const busquedaId = document.getElementById('buscarProductoId').value.trim();
        
        if (busquedaNombre || busquedaId) {
            tbody.innerHTML = '<tr><td colspan="6" class="text-center py-4"><i class="fas fa-search fa-2x text-muted mb-2 d-block"></i><p class="text-muted">No se encontraron productos con ese criterio de búsqueda</p></td></tr>';
        } else {
            tbody.innerHTML = '<tr><td colspan="6" class="text-center">No hay productos registrados</td></tr>';
        }
        return;
    }
    
    const puedeEditar = permisos.includes('editar');
    const puedeEliminar = permisos.includes('eliminar');
    
    tbody.innerHTML = productosAMostrar.map(producto => `
        <tr>
            <td><strong>${producto.nombre}</strong></td>
            <td>${producto.descripcion || 'N/A'}</td>
            <td><span class="badge-precio">$${producto.precio.toFixed(2)}/lb</span></td>
            <td><span class="badge-stock-display">${parseFloat(producto.stock).toFixed(2)} lbs</span></td>
            <td><span class="badge-proveedor">${producto.proveedor_nombre}</span></td>
            <td class="text-center">
                <button class="btn-action-clean btn-info" onclick="verDetalleProducto('${producto._id}')" title="Ver detalle">
                    <i class="fas fa-eye"></i>
                </button>
                ${puedeEditar ? `
                <button class="btn-action-clean btn-warning" onclick="editarProducto('${producto._id}')" title="Editar">
                    <i class="fas fa-edit"></i>
                </button>
                ` : ''}
                ${puedeEliminar ? `
                <button class="btn-action-clean btn-danger" onclick="eliminarProducto('${producto._id}')" title="Eliminar">
                    <i class="fas fa-trash"></i>
                </button>
                ` : ''}
            </td>
        </tr>
    `).join('');
}

function limpiarBusqueda() {
    document.getElementById('buscarProductoNombre').value = '';
    document.getElementById('buscarProductoId').value = '';
    productosFiltrados = productos;
    mostrarProductos();
}
