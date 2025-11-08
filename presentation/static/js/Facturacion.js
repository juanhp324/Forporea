let productos = [];
let productosAgregados = [];
let facturas = [];
let permisos = {};

document.addEventListener('DOMContentLoaded', async function() {
    await cargarPermisos();
    cargarProductos();
});

async function cargarPermisos() {
    try {
        const response = await fetch('/get_user_info');
        const result = await response.json();
        if (result.success && result.permisos) {
            permisos = result.permisos.facturacion || [];
            
            // Solo deshabilitar si explícitamente NO tiene permiso de crear
            if (permisos.length > 0 && !permisos.includes('crear')) {
                setTimeout(() => {
                    const btnCrear = document.querySelector('button[onclick="crearFactura()"]');
                    const btnAgregar = document.querySelector('button[onclick="agregarProducto()"]');
                    if (btnCrear) btnCrear.disabled = true;
                    if (btnAgregar) btnAgregar.disabled = true;
                    const clienteInput = document.getElementById('clienteNombre');
                    const productoSelect = document.getElementById('productoSelect');
                    const cantidadInput = document.getElementById('productoCantidad');
                    if (clienteInput) clienteInput.disabled = true;
                    if (productoSelect) productoSelect.disabled = true;
                    if (cantidadInput) cantidadInput.disabled = true;
                }, 100);
            }
        }
    } catch (error) {
        // Error silencioso - permitir uso por defecto
    }
}

async function cargarProductos() {
    try {
        const response = await fetch('/get_productos_factura');
        const result = await response.json();
        
        if (result.success) {
            productos = result.productos;
            llenarSelectProductos();
        }
    } catch (error) {
        // Error silencioso
    }
}

function llenarSelectProductos() {
    const select = document.getElementById('productoSelect');
    select.innerHTML = '<option value="">Seleccione un producto</option>';
    
    productos.forEach(producto => {
        const option = document.createElement('option');
        option.value = producto._id;
        option.textContent = `${producto.nombre} - $${producto.precio.toFixed(2)} (Stock: ${producto.stock})`;
        option.dataset.precio = producto.precio;
        option.dataset.stock = producto.stock;
        option.dataset.nombre = producto.nombre;
        select.appendChild(option);
    });
}

function agregarProducto() {
    const select = document.getElementById('productoSelect');
    const cantidad = parseInt(document.getElementById('productoCantidad').value);
    
    if (!select.value || !cantidad || cantidad <= 0) {
        showNotification('Selecciona un producto y una cantidad válida', 'warning');
        return;
    }
    
    const option = select.options[select.selectedIndex];
    const productoId = select.value;
    const nombre = option.dataset.nombre;
    const precio = parseFloat(option.dataset.precio);
    const stock = parseInt(option.dataset.stock);
    
    if (cantidad > stock) {
        showNotification('No hay suficiente stock disponible', 'error');
        return;
    }
    
    const productoExistente = productosAgregados.find(p => p.producto_id === productoId);
    if (productoExistente) {
        productoExistente.cantidad += cantidad;
    } else {
        productosAgregados.push({
            producto_id: productoId,
            nombre: nombre,
            precio: precio,
            cantidad: cantidad
        });
    }
    
    mostrarProductosAgregados();
    calcularTotal();
    
    select.value = '';
    document.getElementById('productoCantidad').value = 1;
}

function mostrarProductosAgregados() {
    const tbody = document.getElementById('productosAgregados');
    
    if (productosAgregados.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" class="text-center text-muted">No hay productos agregados</td></tr>';
        return;
    }
    
    tbody.innerHTML = productosAgregados.map((producto, index) => `
        <tr>
            <td>${producto.nombre}</td>
            <td>${producto.cantidad}</td>
            <td>$${producto.precio.toFixed(2)}</td>
            <td>$${(producto.precio * producto.cantidad).toFixed(2)}</td>
            <td>
                <button class="btn btn-danger btn-sm" onclick="eliminarProductoAgregado(${index})">
                    <i class="fas fa-trash"></i>
                </button>
            </td>
        </tr>
    `).join('');
}

function eliminarProductoAgregado(index) {
    productosAgregados.splice(index, 1);
    mostrarProductosAgregados();
    calcularTotal();
}

function calcularTotal() {
    const total = productosAgregados.reduce((sum, producto) => {
        return sum + (producto.precio * producto.cantidad);
    }, 0);
    
    document.getElementById('totalFactura').textContent = total.toFixed(2);
}

async function crearFactura() {
    const cliente = document.getElementById('clienteNombre').value;
    
    if (!cliente) {
        showNotification('Por favor ingresa el nombre del cliente', 'warning');
        return;
    }
    
    if (productosAgregados.length === 0) {
        showNotification('Debes agregar al menos un producto', 'warning');
        return;
    }
    
    const data = {
        cliente: cliente,
        productos: productosAgregados
    };
    
    try {
        const response = await fetch('/create_factura', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.success) {
            showNotification(`Factura creada exitosamente. Total: $${result.total.toFixed(2)}`, 'success');
            
            // Descargar PDF automáticamente
            window.open(`/descargar_factura/${result.factura_id}`, '_blank');
            
            document.getElementById('formFactura').reset();
            productosAgregados = [];
            mostrarProductosAgregados();
            calcularTotal();
            cargarProductos(); // Recargar productos para actualizar stock
        } else {
            showNotification(result.message, 'error');
        }
    } catch (error) {
        showNotification('Error al crear factura', 'error');
    }
}

