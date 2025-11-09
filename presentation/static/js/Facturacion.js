let productos = [];
let productosAgregados = [];
let facturas = [];
let permisos = {};

document.addEventListener('DOMContentLoaded', async function() {
    await cargarPermisos();
    cargarProductos();
    configurarBusqueda();
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

function llenarSelectProductos(filtro = '', selectId = 'productoSelect', buscarPor = 'nombre') {
    const select = document.getElementById(selectId);
    select.innerHTML = '';
    
    let productosFiltrados;
    
    if (buscarPor === 'nombre') {
        productosFiltrados = productos.filter(producto => 
            producto.nombre.toLowerCase().includes(filtro.toLowerCase())
        );
    } else {
        // Búsqueda por ID
        productosFiltrados = productos.filter(producto => 
            producto._id.toLowerCase().includes(filtro.toLowerCase())
        );
    }
    
    if (productosFiltrados.length === 0) {
        const option = document.createElement('option');
        option.value = '';
        option.textContent = 'No se encontraron productos';
        option.disabled = true;
        select.appendChild(option);
        return;
    }
    
    productosFiltrados.forEach(producto => {
        const option = document.createElement('option');
        option.value = producto._id;
        
        // Mostrar nombre o ID según el tipo de búsqueda
        if (buscarPor === 'nombre') {
            option.textContent = producto.nombre;
        } else {
            option.textContent = `${producto._id.substring(0, 8)}... - ${producto.nombre}`;
        }
        
        option.dataset.precio = producto.precio;
        option.dataset.stock = producto.stock;
        option.dataset.nombre = producto.nombre;
        option.dataset.productoId = producto._id;
        select.appendChild(option);
    });
}

function configurarBusqueda() {
    const buscarInput = document.getElementById('buscarProducto');
    const buscarInputId = document.getElementById('buscarProductoId');
    const select = document.getElementById('productoSelect');
    const selectId = document.getElementById('productoSelectId');
    const infoProducto = document.getElementById('infoProducto');
    
    // Evento de búsqueda por NOMBRE
    buscarInput.addEventListener('input', function() {
        const filtro = this.value.trim();
        
        if (filtro.length > 0) {
            llenarSelectProductos(filtro, 'productoSelect', 'nombre');
            select.style.display = 'block';
            selectId.style.display = 'none';
        } else {
            select.style.display = 'none';
            ocultarInfoProducto();
        }
    });
    
    // Evento de búsqueda por ID
    buscarInputId.addEventListener('input', function() {
        const filtro = this.value.trim();
        
        if (filtro.length > 0) {
            llenarSelectProductos(filtro, 'productoSelectId', 'id');
            selectId.style.display = 'block';
            select.style.display = 'none';
        } else {
            selectId.style.display = 'none';
            ocultarInfoProducto();
        }
    });
    
    // Navegación con teclado en búsqueda por nombre
    buscarInput.addEventListener('keydown', function(e) {
        if (select.style.display === 'block') {
            if (e.key === 'ArrowDown') {
                e.preventDefault();
                select.focus();
                select.selectedIndex = 0;
            } else if (e.key === 'Enter' && select.options.length > 0) {
                e.preventDefault();
                select.selectedIndex = 0;
                select.dispatchEvent(new Event('change'));
            }
        }
    });
    
    // Navegación con teclado en búsqueda por ID
    buscarInputId.addEventListener('keydown', function(e) {
        if (selectId.style.display === 'block') {
            if (e.key === 'ArrowDown') {
                e.preventDefault();
                selectId.focus();
                selectId.selectedIndex = 0;
            } else if (e.key === 'Enter' && selectId.options.length > 0) {
                e.preventDefault();
                selectId.selectedIndex = 0;
                selectId.dispatchEvent(new Event('change'));
            }
        }
    });
    
    // Evento al seleccionar un producto por NOMBRE
    select.addEventListener('change', function() {
        if (this.value) {
            const option = this.options[this.selectedIndex];
            mostrarInfoProducto(option);
            buscarInput.value = option.dataset.nombre;
            buscarInputId.value = option.dataset.productoId; // Sincronizar con ID
            select.style.display = 'none';
        }
    });
    
    // Evento al seleccionar un producto por ID
    selectId.addEventListener('change', function() {
        if (this.value) {
            const option = this.options[this.selectedIndex];
            mostrarInfoProducto(option);
            buscarInput.value = option.dataset.nombre; // Sincronizar con nombre
            buscarInputId.value = option.dataset.productoId;
            selectId.style.display = 'none';
        }
    });
    
    // Navegación con Enter en los selects
    select.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && this.value) {
            e.preventDefault();
            this.dispatchEvent(new Event('change'));
        }
    });
    
    selectId.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && this.value) {
            e.preventDefault();
            this.dispatchEvent(new Event('change'));
        }
    });
    
    // Cerrar los selects al hacer clic fuera
    document.addEventListener('click', function(e) {
        if (!buscarInput.contains(e.target) && !select.contains(e.target)) {
            select.style.display = 'none';
        }
        if (!buscarInputId.contains(e.target) && !selectId.contains(e.target)) {
            selectId.style.display = 'none';
        }
    });
}

function mostrarInfoProducto(option) {
    const precio = parseFloat(option.dataset.precio);
    const stock = parseFloat(option.dataset.stock);
    
    document.getElementById('productoPrecioInfo').textContent = `$${precio.toFixed(2)}`;
    document.getElementById('productoStockInfo').textContent = `${stock.toFixed(2)} lbs`;
    document.getElementById('infoProducto').style.display = 'block';
    
    // Enfocar el campo de cantidad
    document.getElementById('productoCantidad').focus();
}

function ocultarInfoProducto() {
    document.getElementById('infoProducto').style.display = 'none';
    document.getElementById('productoPrecioInfo').textContent = '$0.00';
    document.getElementById('productoStockInfo').textContent = '0.00 lbs';
    document.getElementById('buscarProducto').value = '';
    document.getElementById('buscarProductoId').value = '';
}

function agregarProducto() {
    const select = document.getElementById('productoSelect');
    const selectId = document.getElementById('productoSelectId');
    const cantidad = parseFloat(document.getElementById('productoCantidad').value);
    const buscarInput = document.getElementById('buscarProducto');
    
    // Determinar cuál select tiene un valor seleccionado
    const selectActivo = select.value ? select : (selectId.value ? selectId : null);
    
    if (!selectActivo || !selectActivo.value || !cantidad || cantidad <= 0) {
        showNotification('Selecciona un producto y una cantidad válida (en libras)', 'warning');
        return;
    }
    
    const option = selectActivo.options[selectActivo.selectedIndex];
    const productoId = selectActivo.value;
    const nombre = option.dataset.nombre;
    const precio = parseFloat(option.dataset.precio);
    const stock = parseFloat(option.dataset.stock);
    
    // Verificar stock considerando lo que ya está en el carrito
    const productoExistente = productosAgregados.find(p => p.producto_id === productoId);
    const cantidadEnCarrito = productoExistente ? productoExistente.cantidad : 0;
    const cantidadTotal = cantidadEnCarrito + cantidad;
    
    if (cantidadTotal > stock) {
        const disponible = stock - cantidadEnCarrito;
        showNotification(`Stock insuficiente. Solo hay ${disponible.toFixed(2)} lbs disponibles (ya tienes ${cantidadEnCarrito.toFixed(2)} lbs en el carrito)`, 'error');
        return;
    }
    
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
    
    // Limpiar campos
    select.value = '';
    selectId.value = '';
    document.getElementById('productoCantidad').value = 1;
    ocultarInfoProducto();
    buscarInput.focus();
    
    showNotification(`${nombre} agregado al carrito (${cantidad.toFixed(2)} lbs)`, 'success');
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
            <td class="text-center">${producto.cantidad.toFixed(2)} lbs</td>
            <td class="text-end">$${producto.precio.toFixed(2)}</td>
            <td class="text-end">$${(producto.precio * producto.cantidad).toFixed(2)}</td>
            <td class="text-center">
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

