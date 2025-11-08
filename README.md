# Sistema de Gestión de Embutidos - Forporea

Sistema integral para la gestión de productos, proveedores y facturación de embutidos.

## Características

- ✅ **Autenticación de usuarios** con control de sesiones
- ✅ **Gestión de productos** con información detallada y stock
- ✅ **Gestión de proveedores** con datos completos de contacto
- ✅ **Sistema de facturación** con múltiples productos
- ✅ **Modal de detalle** que muestra información completa del producto y proveedor
- ✅ **Interfaz moderna y responsiva** con Bootstrap 5

## Estructura del Proyecto

```
Aplicacion/
├── presentation/          # Capa de presentación
│   ├── templates/        # Plantillas HTML
│   │   ├── Auth/        # Login
│   │   ├── Inicio.html
│   │   ├── Productos.html
│   │   ├── Proveedores.html
│   │   └── Facturacion.html
│   └── static/          # Recursos estáticos
│       ├── css/         # Estilos CSS
│       └── js/          # Scripts JavaScript
├── application/          # Capa de aplicación
│   └── routes/          # Rutas (Blueprints)
│       ├── RAuth.py
│       ├── RInicio.py
│       ├── RProductos.py
│       ├── RProveedores.py
│       └── RFacturacion.py
├── domain/              # Capa de dominio (Validaciones)
│   ├── VAuth.py
│   ├── VProductos.py
│   ├── VProveedores.py
│   └── VFacturacion.py
├── infrasture/          # Capa de infraestructura
│   └── model/          # Modelos y conexiones MongoDB
│       ├── MAuth.py
│       ├── MInicio.py
│       ├── MProductos.py
│       ├── MProveedores.py
│       └── MFacturacion.py
├── app.py              # Punto de entrada
├── requirements.txt    # Dependencias
└── README.md          # Este archivo
```

## Tecnologías

- **Backend**: Python 3.x + Flask
- **Base de Datos**: MongoDB
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5, Font Awesome
- **Arquitectura**: Capas (Presentation, Application, Domain, Infrastructure)

## Instalación

1. **Clonar o descargar el proyecto**

2. **Crear entorno virtual**
```bash
python -m venv .venv
```

3. **Activar entorno virtual**
- Windows:
```bash
.venv\Scripts\activate
```
- Linux/Mac:
```bash
source .venv/bin/activate
```

4. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

5. **Configurar MongoDB**
- Asegúrate de tener MongoDB instalado y corriendo en `localhost:27017`
- La base de datos se llamará `Forporea`

6. **Crear datos de prueba en MongoDB**

```javascript
// Conectar a MongoDB
use Forporea

// Crear usuario de prueba
db.usuarios.insertOne({
    nombre: "Administrador",
    email: "admin@forporea.com",
    password: "admin123",
    rol: "admin"
})

// Crear proveedor de prueba
db.proveedores.insertOne({
    nombre: "Embutidos del Norte",
    contacto: "Juan Pérez",
    telefono: "555-1234",
    email: "contacto@embutidosnorte.com",
    direccion: "Calle Principal 123"
})

// Obtener el ID del proveedor creado y crear producto de prueba
// Reemplaza PROVEEDOR_ID con el ObjectId del proveedor
db.productos.insertOne({
    nombre: "Chorizo Parrillero",
    descripcion: "Chorizo premium para parrilla",
    precio: 15.50,
    stock: 100,
    proveedor_id: ObjectId("PROVEEDOR_ID")
})
```

## Ejecución

```bash
python app.py
```

La aplicación estará disponible en: `http://localhost:5000`

## Credenciales de Prueba

- **Email**: admin@forporea.com
- **Password**: admin123

## Módulos del Sistema

### 1. Login
- Autenticación segura de usuarios
- Validación de credenciales
- Control de sesiones

### 2. Inicio
- Dashboard con información del usuario
- Accesos rápidos a módulos
- Resumen de operaciones

### 3. Productos
- Listar todos los productos
- Crear nuevos productos
- Editar productos existentes
- Eliminar productos
- **Ver detalle completo** (modal con info del producto y proveedor)

### 4. Proveedores
- Listar todos los proveedores
- Crear nuevos proveedores
- Editar proveedores existentes
- Eliminar proveedores

### 5. Facturación
- Crear facturas con múltiples productos
- Selección de productos del inventario
- Cálculo automático de totales
- Historial de facturas

## Convenciones de Nomenclatura

- **Rutas**: Archivos comienzan con `R` mayúscula (ej: `RProductos.py`)
- **Validadores**: Archivos comienzan con `V` mayúscula (ej: `VProductos.py`)
- **Modelos**: Archivos comienzan con `M` mayúscula (ej: `MProductos.py`)

## Arquitectura en Capas

1. **Presentation**: Interfaz de usuario (HTML, CSS, JS)
2. **Application**: Rutas y orquestación (Flask Blueprints)
3. **Domain**: Validaciones y reglas de negocio
4. **Infrastructure**: Conexiones a base de datos (MongoDB)

## Notas Importantes

- Todas las validaciones se realizan en la capa `domain`
- La conexión a MongoDB está en la capa `infrasture/model`
- Los templates HTML están en `presentation/templates`
- Los archivos estáticos (CSS/JS) están en `presentation/static`
- El archivo `app.py` registra todos los blueprints y aplica `authValidator(app)`

## Soporte

Para consultas o soporte, contactar al equipo de desarrollo.

---

**Forporea - Sistema de Gestión de Embutidos**
*Versión 1.0 - 2024*
