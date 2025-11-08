let productos = [];
let productosAgregados = [];
let facturas = [];

document.addEventListener('DOMContentLoaded', function() {
    cargarProductos();
    cargarFacturas();
});

async function cargarProductos() {
    try {
        const response = await fetch('/get_productos_factura');
        const result = await response.json();
        
        if (result.success) {
            productos = result.productos;
            llenarSelectProductos();
        }
    } catch (error) {
        console.error('Error:', error);
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
        alert('Selecciona un producto y una cantidad válida');
        return;
    }
    
    const option = select.options[select.selectedIndex];
    const productoId = select.value;
    const nombre = option.dataset.nombre;
    const precio = parseFloat(option.dataset.precio);
    const stock = parseInt(option.dataset.stock);
    
    if (cantidad > stock) {
        alert('No hay suficiente stock disponible');
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
        alert('Por favor ingresa el nombre del cliente');
        return;
    }
    
    if (productosAgregados.length === 0) {
        alert('Debes agregar al menos un producto');
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
            alert(`Factura creada exitosamente. Total: $${result.total.toFixed(2)}`);
            
            // Descargar PDF automáticamente
            window.open(`/descargar_factura/${result.factura_id}`, '_blank');
            
            document.getElementById('formFactura').reset();
            productosAgregados = [];
            mostrarProductosAgregados();
            calcularTotal();
            cargarFacturas();
            cargarProductos(); // Recargar productos para actualizar stock
        } else {
            alert(result.message);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error al crear factura');
    }
}

async function cargarFacturas() {
    try {
        const response = await fetch('/get_facturas');
        const result = await response.json();
        
        if (result.success) {
            facturas = result.facturas;
            mostrarFacturas();
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

function mostrarFacturas() {
    const container = document.getElementById('listaFacturas');
    
    if (facturas.length === 0) {
        container.innerHTML = '<p class="text-center text-muted">No hay facturas registradas</p>';
        return;
    }
    
    container.innerHTML = facturas.map(factura => `
        <div class="factura-item">
            <div class="d-flex justify-content-between align-items-start">
                <div>
                    <h6><i class="fas fa-file-invoice me-2"></i>${factura.cliente}</h6>
                    <small class="d-block"><i class="fas fa-calendar me-1"></i>${factura.fecha}</small>
                    <small class="d-block"><i class="fas fa-dollar-sign me-1"></i>Total: $${factura.total.toFixed(2)}</small>
                    <small class="d-block"><i class="fas fa-box me-1"></i>${factura.productos.length} producto(s)</small>
                </div>
                <button class="btn btn-sm btn-primary" onclick="descargarFacturaPDF('${factura._id}')" title="Descargar PDF">
                    <i class="fas fa-download"></i>
                </button>
            </div>
        </div>
    `).join('');
}

function descargarFacturaPDF(facturaId) {
    window.open(`/descargar_factura/${facturaId}`, '_blank');
}
