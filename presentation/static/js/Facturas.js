let facturas = [];
let facturasFiltradas = [];
let currentFacturaId = null;
let datepickerDesde = null;
let datepickerHasta = null;

document.addEventListener('DOMContentLoaded', function() {
    cargarFacturas();
    inicializarDatepickers();
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
            <td><strong>${factura.cliente || 'Sin cliente'}</strong></td>
            <td>${factura.fecha || 'Sin fecha'}</td>
            <td><span class="badge-total">$${(factura.total || 0).toFixed(2)}</span></td>
            <td><span class="badge bg-info">${(factura.productos || []).length} producto(s)</span></td>
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

// ============================================
// FUNCIONALIDAD DE BÚSQUEDA POR FECHA
// ============================================

function inicializarDatepickers() {
    const localeEs = {
        days: ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'],
        daysShort: ['Dom', 'Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb'],
        daysMin: ['Do', 'Lu', 'Ma', 'Mi', 'Ju', 'Vi', 'Sá'],
        months: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
        monthsShort: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
        today: 'Hoy',
        clear: 'Limpiar',
        dateFormat: 'dd/MM/yyyy',
        timeFormat: 'HH:mm',
        firstDay: 1
    };
    
    // Inicializar Air Datepicker para "Desde"
    datepickerDesde = new AirDatepicker('#fechaDesde', {
        locale: localeEs,
        dateFormat: 'dd/MM/yyyy',
        autoClose: true,
        onSelect: ({date}) => {
            if (datepickerHasta && date) {
                datepickerHasta.update({minDate: date});
            }
        }
    });
    
    // Inicializar Air Datepicker para "Hasta"
    datepickerHasta = new AirDatepicker('#fechaHasta', {
        locale: localeEs,
        dateFormat: 'dd/MM/yyyy',
        autoClose: true,
        onSelect: ({date}) => {
            if (datepickerDesde && date) {
                datepickerDesde.update({maxDate: date});
            }
        }
    });
}

function buscarPorFecha() {
    const fechaDesdeStr = document.getElementById('fechaDesde').value;
    const fechaHastaStr = document.getElementById('fechaHasta').value;
    
    if (!fechaDesdeStr && !fechaHastaStr) {
        facturasFiltradas = facturas;
        mostrarFacturasFiltradas();
        return;
    }
    
    facturasFiltradas = facturas.filter(factura => {
        // Convertir la fecha de la factura a formato comparable
        const fechaFactura = parsearFecha(factura.fecha);
        
        if (!fechaFactura) return false;
        
        // Convertir las fechas de búsqueda a objetos Date en hora local
        let desde = null;
        let hasta = null;
        
        if (fechaDesdeStr) {
            // Formato DD/MM/YYYY de Flatpickr
            const [dia, mes, anio] = fechaDesdeStr.split('/');
            desde = new Date(parseInt(anio), parseInt(mes) - 1, parseInt(dia), 0, 0, 0, 0);
        }
        
        if (fechaHastaStr) {
            // Formato DD/MM/YYYY de Flatpickr
            const [dia, mes, anio] = fechaHastaStr.split('/');
            hasta = new Date(parseInt(anio), parseInt(mes) - 1, parseInt(dia), 23, 59, 59, 999);
        }
        
        // Filtrar según el rango
        if (desde && hasta) {
            return fechaFactura >= desde && fechaFactura <= hasta;
        } else if (desde) {
            return fechaFactura >= desde;
        } else if (hasta) {
            return fechaFactura <= hasta;
        }
        
        return true;
    });
    
    mostrarFacturasFiltradas();
}

function parsearFecha(fechaStr) {
    // Intentar parsear diferentes formatos de fecha
    // Formato esperado: "DD/MM/YYYY HH:MM" o similar
    try {
        // Si viene en formato "DD/MM/YYYY HH:MM"
        const partes = fechaStr.split(' ');
        const fecha = partes[0].split('/');
        
        if (fecha.length === 3) {
            const dia = parseInt(fecha[0]);
            const mes = parseInt(fecha[1]) - 1; // Los meses en JS van de 0-11
            const anio = parseInt(fecha[2]);
            
            let hora = 0, minuto = 0;
            if (partes[1]) {
                const tiempo = partes[1].split(':');
                hora = parseInt(tiempo[0]) || 0;
                minuto = parseInt(tiempo[1]) || 0;
            }
            
            return new Date(anio, mes, dia, hora, minuto);
        }
        
        // Intentar parsear directamente
        return new Date(fechaStr);
    } catch (error) {
        return null;
    }
}

function mostrarFacturasFiltradas() {
    const tbody = document.getElementById('tablaFacturas');
    const facturasAMostrar = facturasFiltradas.length > 0 || 
                             document.getElementById('fechaDesde').value || 
                             document.getElementById('fechaHasta').value 
                             ? facturasFiltradas : facturas;
    
    if (facturasAMostrar.length === 0) {
        const fechaDesde = document.getElementById('fechaDesde').value;
        const fechaHasta = document.getElementById('fechaHasta').value;
        
        if (fechaDesde || fechaHasta) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="5" class="text-center py-5">
                        <i class="fas fa-calendar-times fa-2x text-muted mb-3"></i>
                        <p class="text-muted">No se encontraron facturas en el rango de fechas seleccionado</p>
                    </td>
                </tr>`;
            mobileContainer.innerHTML = `
                <div class="text-center py-5">
                    <i class="fas fa-calendar-times fa-2x text-muted mb-3"></i>
                    <p class="text-muted">No se encontraron facturas en el rango de fechas seleccionado</p>
                </div>`;
        } else {
            tbody.innerHTML = `
                <tr>
                    <td colspan="5" class="text-center py-5">
                        <i class="fas fa-inbox fa-2x text-muted mb-3"></i>
                        <p class="text-muted">No hay facturas registradas</p>
                    </td>
                </tr>`;
            mobileContainer.innerHTML = `
                <div class="text-center py-5">
                    <i class="fas fa-inbox fa-2x text-muted mb-3"></i>
                    <p class="text-muted">No hay facturas registradas</p>
                </div>`;
        }
        return;
    }
    
    // Versión Desktop (Tabla)
    tbody.innerHTML = facturasAMostrar.map(factura => `
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
    
    // Versión Móvil (Cards)
    mobileContainer.innerHTML = facturasAMostrar.map(factura => `
        <div class="mobile-card">
            <div class="mobile-card-header">
                <div class="mobile-card-title">${factura.cliente}</div>
                <span class="badge bg-success">$${factura.total.toFixed(2)}</span>
            </div>
            <div class="mobile-card-body">
                <div class="mobile-card-row">
                    <span class="mobile-card-label"><i class="fas fa-calendar me-1"></i>Fecha</span>
                    <span class="mobile-card-value">${factura.fecha}</span>
                </div>
                <div class="mobile-card-row">
                    <span class="mobile-card-label"><i class="fas fa-box me-1"></i>Productos</span>
                    <span class="mobile-card-value">${factura.productos.length} producto(s)</span>
                </div>
                <div class="mobile-card-row">
                    <span class="mobile-card-label"><i class="fas fa-dollar-sign me-1"></i>Total</span>
                    <span class="mobile-card-value text-success fw-bold">$${factura.total.toFixed(2)}</span>
                </div>
            </div>
            <div class="mobile-card-actions">
                <button class="btn btn-sm btn-info" onclick="verDetalleFactura('${factura._id}')">
                    <i class="fas fa-eye me-1"></i>Ver Detalle
                </button>
                <button class="btn btn-sm btn-success" onclick="descargarFacturaPDF('${factura._id}')">
                    <i class="fas fa-download me-1"></i>PDF
                </button>
            </div>
        </div>
    `).join('');
}

function limpiarBusquedaFecha() {
    // Limpiar los inputs directamente
    document.getElementById('fechaDesde').value = '';
    document.getElementById('fechaHasta').value = '';
    
    // Limpiar Air Datepicker de manera segura
    try {
        if (datepickerDesde && datepickerDesde.clear) {
            datepickerDesde.clear();
        }
        if (datepickerDesde && datepickerDesde.update) {
            datepickerDesde.update({maxDate: null});
        }
    } catch (e) {
        // Error al limpiar datepicker desde
    }
    
    try {
        if (datepickerHasta && datepickerHasta.clear) {
            datepickerHasta.clear();
        }
        if (datepickerHasta && datepickerHasta.update) {
            datepickerHasta.update({minDate: null});
        }
    } catch (e) {
        // Error al limpiar datepicker hasta
    }
    
    // Limpiar el filtro
    facturasFiltradas = [];
    
    // Recargar todas las facturas desde el servidor
    cargarFacturas();
}
