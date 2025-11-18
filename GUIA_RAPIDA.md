# 🚀 Guía Rápida - Forporea API REST

## ✅ ¿Qué se hizo?

### Backend (API REST)
- ✅ Convertido a API REST con JWT
- ✅ Eliminadas sesiones de Flask
- ✅ CORS habilitado
- ✅ Rutas protegidas con `@token_required`
- ✅ Endpoints REST (`/api/productos`, `/api/proveedores`, etc.)

### Frontend (HTML + JavaScript)
- ✅ Login sin Jinja2 (usa API)
- ✅ Productos sin Jinja2 (usa API)
- ✅ Proveedores sin Jinja2 (usa API)
- ✅ Inicio sin Jinja2 (usa API)
- ✅ Scripts JS para autenticación y API

## 🎯 Cómo Usar

### 1️⃣ Iniciar Backend (Terminal 1)
```bash
cd /home/programacion2/proyectos/Forporea
source .venv/bin/activate
python app.py
```
✅ Backend corriendo en `http://localhost:5000`

### 2️⃣ Iniciar Frontend (Terminal 2)
```bash
cd /home/programacion2/proyectos/Forporea/presentation
python3 -m http.server 8080
```
✅ Frontend corriendo en `http://localhost:8080`

### 3️⃣ Abrir en el Navegador
```
http://localhost:8080
```

### 4️⃣ Credenciales
```
Email: admin@forporea.com
Password: admin123
```

## 📁 Archivos Importantes

### Nuevos Archivos HTML (Sin Jinja2)
```
presentation/templates/
├── Auth/Login.html          ✅ Modificado
├── Inicio_new.html          ✅ Nuevo
├── Productos_new.html       ✅ Nuevo
└── Proveedores_new.html     ✅ Nuevo
```

### Scripts JavaScript
```
presentation/static/js/
├── auth.js          ✅ Autenticación JWT
├── api.js           ✅ Cliente API REST
├── productos.js     ✅ Lógica productos
└── proveedores.js   ✅ Lógica proveedores
```

### Backend API
```
application/routes/
├── RAuth.py         ✅ Login, logout, refresh
├── RProductos.py    ✅ CRUD productos con JWT
├── RProveedores.py  ✅ CRUD proveedores con JWT
├── RFacturacion.py  ✅ CRUD facturas con JWT
└── RInicio.py       ✅ Info usuario con JWT
```

## 🔥 Flujo de Trabajo

### Login
1. Usuario ingresa email y password
2. Frontend llama a `POST /api/auth/Login`
3. Backend valida y retorna tokens JWT
4. Frontend guarda tokens en localStorage
5. Redirige a `Inicio_new.html`

### Páginas Protegidas
1. Frontend verifica token en localStorage
2. Si no hay token → Redirige a Login
3. Si hay token → Carga datos de la API
4. Agrega token en header `Authorization: Bearer <token>`

### Llamadas a la API
```javascript
// Ejemplo: Obtener productos
const data = await getProductos();
console.log(data.productos);

// Ejemplo: Crear producto
await createProducto({
    nombre: "Chorizo",
    descripcion: "Chorizo español",
    precio: 15.50,
    stock: 100,
    proveedor_id: "123abc"
});
```

## 🎨 Páginas Disponibles

| Página | URL | Estado |
|--------|-----|--------|
| Login | `/templates/Auth/Login.html` | ✅ Funcionando |
| Inicio | `/templates/Inicio_new.html` | ✅ Funcionando |
| Productos | `/templates/Productos_new.html` | ✅ Funcionando |
| Proveedores | `/templates/Proveedores_new.html` | ✅ Funcionando |
| Facturación | - | ⏳ Pendiente |

## 🔧 API Endpoints

### Autenticación
- `POST /api/auth/Login` - Login (público)
- `POST /api/auth/logout` - Logout (público)
- `POST /api/auth/refresh` - Renovar token (público)
- `GET /api/auth/version` - Versión (público)

### Productos (Requiere JWT)
- `GET /api/productos` - Listar
- `GET /api/productos/<id>` - Ver uno
- `POST /api/productos` - Crear (requiere permiso)
- `PUT /api/productos/<id>` - Actualizar (requiere permiso)
- `DELETE /api/productos/<id>` - Eliminar (requiere permiso)

### Proveedores (Requiere JWT)
- `GET /api/proveedores` - Listar
- `GET /api/proveedores/<id>` - Ver uno
- `POST /api/proveedores` - Crear (requiere permiso)
- `PUT /api/proveedores/<id>` - Actualizar (requiere permiso)
- `DELETE /api/proveedores/<id>` - Eliminar (requiere permiso)

### Facturas (Requiere JWT)
- `GET /api/facturas` - Listar
- `POST /api/facturas` - Crear (requiere permiso)
- `GET /api/facturas/<id>/descargar` - Descargar PDF

### Usuario (Requiere JWT)
- `GET /api/user-info` - Info del usuario actual

## 🐛 Solución de Problemas

### Error: "Token no proporcionado"
**Causa:** No estás logueado o el token expiró
**Solución:** Vuelve a hacer login

### Error: "CORS blocked"
**Causa:** Estás abriendo el HTML directamente (`file://`)
**Solución:** Usa el servidor HTTP (`python3 -m http.server 8080`)

### Error: "Failed to fetch"
**Causa:** El backend no está corriendo
**Solución:** Inicia el backend con `python app.py`

### La página no carga datos
**Causa:** Revisa la consola del navegador (F12)
**Solución:** Verifica que:
- Backend esté corriendo
- Frontend esté en servidor HTTP
- Estés logueado

## 📝 Próximos Pasos

1. ✅ Backend API REST funcionando
2. ✅ Login funcionando
3. ✅ Productos funcionando
4. ✅ Proveedores funcionando
5. ⏳ Crear página de Facturación
6. ⏳ Agregar más funcionalidades
7. ⏳ Deploy a producción

## 💡 Notas Importantes

- **Tokens JWT:** Se guardan en localStorage
- **Renovación automática:** Los tokens se renuevan automáticamente
- **Seguridad:** Nunca compartas tu SECRET_KEY
- **CORS:** Ya está configurado en el backend
- **Archivos antiguos:** Los archivos con Jinja2 siguen ahí pero no se usan

## 🎉 ¡Listo!

Tu aplicación ahora funciona como:
- **Backend:** API REST independiente (puerto 5000)
- **Frontend:** HTML + JavaScript (puerto 8080)
- **Comunicación:** JWT tokens en headers HTTP

¿Necesitas ayuda? Revisa:
1. Consola del navegador (F12)
2. Terminal del backend
3. `presentation/README_API.md`
