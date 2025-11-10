# 🚀 Guía de Deployment en Render.com

## 📋 Requisitos Previos

1. Cuenta en GitHub
2. Cuenta en Render.com (gratis)
3. Cuenta en MongoDB Atlas (gratis)

---

## 🗄️ PASO 1: Configurar MongoDB Atlas (Base de Datos en la Nube)

### 1.1 Crear cuenta en MongoDB Atlas
- Ve a: https://www.mongodb.com/cloud/atlas/register
- Regístrate gratis (no necesitas tarjeta de crédito)

### 1.2 Crear un Cluster
1. Click en **"Build a Database"**
2. Selecciona **"M0 FREE"** (cluster gratuito)
3. Elige un proveedor (AWS, Google Cloud o Azure)
4. Selecciona la región más cercana a ti
5. Click en **"Create Cluster"** (tarda 3-5 minutos)

### 1.3 Configurar Acceso
1. **Crear usuario de base de datos:**
   - Ve a **"Database Access"** en el menú lateral
   - Click en **"Add New Database User"**
   - Elige **"Password"** como método de autenticación
   - Usuario: `forporea_user`
   - Password: Genera una contraseña segura (guárdala)
   - Rol: **"Read and write to any database"**
   - Click en **"Add User"**

2. **Permitir acceso desde cualquier IP:**
   - Ve a **"Network Access"** en el menú lateral
   - Click en **"Add IP Address"**
   - Click en **"Allow Access from Anywhere"** (0.0.0.0/0)
   - Click en **"Confirm"**

### 1.4 Obtener la URI de Conexión
1. Ve a **"Database"** en el menú lateral
2. Click en **"Connect"** en tu cluster
3. Selecciona **"Connect your application"**
4. Copia la **Connection String** (URI)
5. Reemplaza `<password>` con tu contraseña real
6. Ejemplo: `mongodb+srv://forporea_user:TU_PASSWORD@cluster0.xxxxx.mongodb.net/`

### 1.5 Cargar Datos Iniciales
1. Ve a **"Database"** → **"Browse Collections"**
2. Click en **"Add My Own Data"**
3. Database name: `Forporea`
4. Collection name: `usuarios`
5. Click en **"Create"**

**Opción A: Usar MongoDB Compass (Recomendado)**
- Descarga MongoDB Compass: https://www.mongodb.com/try/download/compass
- Conecta usando tu URI
- Ejecuta el script `Database.py` modificando la URI

**Opción B: Desde la web**
- Crea las colecciones manualmente: `usuarios`, `productos`, `proveedores`, `facturas`
- Inserta documentos uno por uno

---

## 🐙 PASO 2: Subir Proyecto a GitHub

### 2.1 Inicializar Git (si no lo has hecho)
```bash
git init
git add .
git commit -m "Preparar proyecto para deployment"
```

### 2.2 Crear Repositorio en GitHub
1. Ve a: https://github.com/new
2. Nombre: `Forporea`
3. Visibilidad: **Privado** o **Público**
4. NO inicialices con README (ya tienes uno)
5. Click en **"Create repository"**

### 2.3 Subir Código
```bash
git remote add origin https://github.com/TU_USUARIO/Forporea.git
git branch -M main
git push -u origin main
```

---

## 🌐 PASO 3: Desplegar en Render.com

### 3.1 Crear Cuenta en Render
- Ve a: https://render.com/
- Regístrate con tu cuenta de GitHub

### 3.2 Crear Web Service
1. Click en **"New +"** → **"Web Service"**
2. Conecta tu repositorio de GitHub
3. Selecciona el repositorio **"Forporea"**
4. Click en **"Connect"**

### 3.3 Configurar el Servicio
Completa los siguientes campos:

- **Name**: `forporea` (o el nombre que prefieras)
- **Region**: Selecciona la más cercana
- **Branch**: `main`
- **Root Directory**: (dejar vacío)
- **Runtime**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app`
- **Instance Type**: `Free`

### 3.4 Agregar Variables de Entorno
En la sección **"Environment Variables"**, agrega:

1. Click en **"Add Environment Variable"**
2. Agrega estas variables:

```
MONGODB_URI = mongodb+srv://forporea_user:TU_PASSWORD@cluster0.xxxxx.mongodb.net/
DATABASE_NAME = Forporea
```

⚠️ **IMPORTANTE**: Reemplaza `TU_PASSWORD` y la URI completa con tus datos reales de MongoDB Atlas.

### 3.5 Desplegar
1. Click en **"Create Web Service"**
2. Render comenzará a construir y desplegar tu aplicación
3. Espera 3-5 minutos

---

## ✅ PASO 4: Verificar el Deployment

### 4.1 Acceder a tu Aplicación
- URL: `https://forporea.onrender.com` (o el nombre que elegiste)
- Render te mostrará la URL en la parte superior

### 4.2 Probar Login
- Usuario: `admin@forporea.com`
- Password: `admin123`

### 4.3 Ver Logs
- En Render, ve a la pestaña **"Logs"**
- Aquí verás si hay errores

---

## 🔧 Solución de Problemas Comunes

### ❌ Error: "Application failed to respond"
**Causa**: Render no puede conectarse a MongoDB

**Solución**:
1. Verifica que la URI de MongoDB sea correcta
2. Verifica que permitiste acceso desde cualquier IP (0.0.0.0/0)
3. Verifica que el usuario y contraseña sean correctos

### ❌ Error: "Build failed"
**Causa**: Problemas con las dependencias

**Solución**:
1. Verifica que `requirements.txt` tenga todas las dependencias
2. Verifica que `Procfile` exista y tenga: `web: gunicorn app:app`

### ❌ La aplicación se carga pero no hay datos
**Causa**: La base de datos está vacía

**Solución**:
1. Ejecuta el script `Database.py` con la URI de MongoDB Atlas
2. O inserta los datos manualmente en MongoDB Atlas

---

## 🔄 Actualizar la Aplicación

Cada vez que hagas cambios:

```bash
git add .
git commit -m "Descripción de los cambios"
git push
```

Render detectará los cambios automáticamente y volverá a desplegar.

---

## 💰 Costos

- **MongoDB Atlas (M0)**: Gratis para siempre
  - 512 MB de almacenamiento
  - Conexiones compartidas
  - Suficiente para desarrollo y proyectos pequeños

- **Render.com (Free Tier)**: Gratis
  - 750 horas/mes
  - 512 MB RAM
  - La app se "duerme" después de 15 minutos de inactividad
  - Tarda ~30 segundos en "despertar" al recibir una petición

---

## 🚀 Mejoras para Producción (Opcional)

### Dominio Personalizado
1. En Render, ve a **"Settings"** → **"Custom Domain"**
2. Agrega tu dominio (ej: `www.forporea.com`)
3. Configura los DNS según las instrucciones

### Plan de Pago (Recomendado para producción)
- **Render**: $7/mes (sin "sleep", mejor rendimiento)
- **MongoDB Atlas**: $9/mes (M10, mejor rendimiento)

---

## 📞 Soporte

Si tienes problemas:
1. Revisa los **Logs** en Render
2. Verifica las **Variables de Entorno**
3. Verifica la conexión a MongoDB Atlas

---

## 🎉 ¡Listo!

Tu aplicación ahora está en línea y accesible desde cualquier lugar del mundo.

**URL de ejemplo**: https://forporea.onrender.com

---

## 📝 Checklist Final

- [ ] MongoDB Atlas configurado
- [ ] Usuario de base de datos creado
- [ ] IP 0.0.0.0/0 permitida
- [ ] Datos iniciales cargados
- [ ] Repositorio en GitHub
- [ ] Web Service creado en Render
- [ ] Variables de entorno configuradas
- [ ] Aplicación desplegada exitosamente
- [ ] Login funciona correctamente
