let facturas = [];
let currentFacturaId = null;

document.addEventListener('DOMContentLoaded', function() {
    cargarFacturas();
});

async function cargarFacturas() {
    try {
        const response = await fetch('/get_facturas');
        const result = await response.json();
        
        if (result.success) {
            facturas = result.facturas;
            mostrarFacturas();
        } else {
            const tbody = document.getElementById('tablaFacturas');
            tbody.innerHTML = `<tr><td colspan="5" class="text-center text-danger"><i class="fas fa-exclamation-circle me-2"></i>Error: ${result.message}</td></tr>`;
        }
    } catch (error) {
        const tbody = document.getElementById('tablaFacturas');
        tbody.innerHTML = '<tr><td colspan="5" class="text-center text-danger"><i class="fas fa-exclamation-circle me-2"></i>Error al cargar las facturas</td></tr>';
    }
}

function mostrarFacturas() {
    const tbody = document.getElementById('tablaFacturas');
    
    if (facturas.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="5" class="text-center py-5">
                    <i class="fas fa-inbox fa-2x text-muted mb-3"></i>
                    <p class="text-muted">No hay facturas registradas</p>
                </td>
            </tr>`;
        return;
    }
    
    tbody.innerHTML = facturas.map(factura => `
        <tr>
            <td><strong>${factura.cliente}</strong></td>
            <td>${factura.fecha}</td>
            <td><span class="badge-total">$${factura.total.toFixed(2)}</span></td>
            <td><span class="badge bg-info">${factura.productos.length} producto(s)</span></td>
            <td class="text-center">
                <button class="btn-action-clean btn-info" onclick="verDetalleFactura('${factura._id}')" title="Ver detalle">
                    <i class="fas fa-eye"></i>
                </button>
                <button class="btn-action-clean btn-success" onclick="descargarFacturaPDF('${factura._id}')" title="Descargar PDF">
                    <i class="fas fa-download"></i>
                </button>
            </td>
        </tr>
    `).join('');
}

function verDetalleFactura(id) {
    const factura = facturas.find(f => f._id === id);
    if (!factura) return;
    
    currentFacturaId = id;
    
    document.getElementById('detalleCliente').textContent = factura.cliente;
    document.getElementById('detalleFecha').textContent = factura.fecha;
    document.getElementById('detalleTotal').textContent = factura.total.toFixed(2);
    
    const tbody = document.getElementById('detalleProductos');
    tbody.innerHTML = factura.productos.map(prod => `
        <tr>
            <td>${prod.nombre}</td>
            <td>${prod.cantidad}</td>
            <td>$${prod.precio_unitario.toFixed(2)}</td>
            <td><strong>$${prod.subtotal.toFixed(2)}</strong></td>
        </tr>
    `).join('');
    
    const modal = new bootstrap.Modal(document.getElementById('modalDetalleFactura'));
    modal.show();
}

function descargarFacturaPDF(facturaId) {
    window.open(`/descargar_factura/${facturaId}`, '_blank');
}
