document.addEventListener('DOMContentLoaded', async function() {
    await cargarInformacionUsuario();
    await cargarEstadisticas();
});

async function cargarInformacionUsuario() {
    try {
        const response = await fetch('/get_user_info');
        const result = await response.json();
        
        if (result.success) {
            document.getElementById('userName').textContent = result.nombre;
            document.getElementById('user').textContent = result.user;
            document.getElementById('userEmail').textContent = result.email;
            document.getElementById('userRol').textContent = result.rol;
            
            // Actualizar versión en el navbar y dashboard
            if (result.version && result.version.version) {
                const versionElement = document.getElementById('appVersion');
                if (versionElement) {
                    versionElement.textContent = 'v' + result.version.version;
                }
                const dashboardVersionElement = document.getElementById('dashboardVersion');
                if (dashboardVersionElement) {
                    dashboardVersionElement.textContent = result.version.version;
                }
            }
        }
    } catch (error) {
        // Error al cargar información del usuario
    }
}

async function cargarEstadisticas() {
    try {
        // Cargar productos
        const productosResponse = await fetch('/get_productos');
        const productosData = await productosResponse.json();
        if (productosData.success) {
            const productosCount = productosData.productos.length;
            document.getElementById('statsProductos').textContent = productosCount;
        }
        
        // Cargar proveedores
        const proveedoresResponse = await fetch('/get_proveedores');
        const proveedoresData = await proveedoresResponse.json();
        if (proveedoresData.success) {
            const proveedoresCount = proveedoresData.proveedores.length;
            document.getElementById('statsProveedores').textContent = proveedoresCount;
        }
        
        // Cargar facturas
        const facturasResponse = await fetch('/get_facturas');
        const facturasData = await facturasResponse.json();
        if (facturasData.success) {
            // Calcular facturas y ventas de hoy
            const hoy = new Date();
            const hoyStr = `${hoy.getFullYear()}-${String(hoy.getMonth() + 1).padStart(2, '0')}-${String(hoy.getDate()).padStart(2, '0')}`;
            let facturasHoy = 0;
            let ventasHoy = 0;
            
            facturasData.facturas.forEach(factura => {
                // Extraer solo la fecha (YYYY-MM-DD) de la factura
                let facturaFecha = '';
                if (factura.fecha) {
                    // Si viene como "2025-11-09 13:48" o "2025-11-09"
                    facturaFecha = factura.fecha.split(' ')[0];
                }
                
                if (facturaFecha === hoyStr) {
                    facturasHoy++;
                    const total = parseFloat(factura.total || 0);
                    ventasHoy += total;
                }
            });
            
            // Actualizar facturas de hoy
            document.getElementById('statsFacturas').textContent = facturasHoy;
            
            // Actualizar ventas de hoy
            document.getElementById('statsVentas').textContent = 
                '$' + ventasHoy.toLocaleString('es-CO', { minimumFractionDigits: 0, maximumFractionDigits: 0 });
        }
    } catch (error) {
        // Error al cargar estadísticas
    }
}
