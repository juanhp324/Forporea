# 📦 Guía de Versionamiento Semántico

## 🎯 Formato de Versión: X.Y.Z

- **X (Major)**: Cambios incompatibles o grandes refactorizaciones
- **Y (Minor)**: Nuevas funcionalidades compatibles
- **Z (Patch)**: Correcciones de bugs y mejoras menores

## 🚀 Crear una Nueva Versión

### Opción 1: Versión Específica (Recomendado)

```bash
# Después de hacer commit
python create_version.py 1.0.0 "Primera versión estable"
python create_version.py 1.1.0 "Agregar sistema de notificaciones"
python create_version.py 1.1.1 "Corregir bug en login"
python create_version.py 2.0.0 "Rediseño completo de la UI"
```

### Opción 2: Auto-incremento

```bash
# Incrementa automáticamente el patch (0.0.1 → 0.0.2)
python create_version.py
```

## 📋 Ejemplos de Versionamiento

### Versión 0.x.x - Desarrollo Inicial
```bash
python create_version.py 0.1.0 "Estructura básica del proyecto"
python create_version.py 0.2.0 "Sistema de autenticación"
python create_version.py 0.3.0 "CRUD de productos"
python create_version.py 0.3.1 "Fix: Error en validación de productos"
```

### Versión 1.x.x - Primera Versión Estable
```bash
python create_version.py 1.0.0 "Primera versión estable en producción"
python create_version.py 1.1.0 "Agregar módulo de reportes"
python create_version.py 1.1.1 "Fix: Error en cálculo de totales"
python create_version.py 1.2.0 "Agregar exportación a Excel"
```

### Versión 2.x.x - Cambios Mayores
```bash
python create_version.py 2.0.0 "Migración a nueva arquitectura"
python create_version.py 2.1.0 "Nuevo dashboard interactivo"
```

## 🎨 Convenciones de Commits y Versiones

### Patch (x.x.X) - Correcciones
```bash
git commit -m "fix: Corregir error en cálculo de stock"
python create_version.py 1.0.1 "Corrección de bug en stock"
```

### Minor (x.X.x) - Nuevas Funcionalidades
```bash
git commit -m "feat: Agregar filtros avanzados en productos"
python create_version.py 1.1.0 "Filtros avanzados"
```

### Major (X.x.x) - Cambios Importantes
```bash
git commit -m "refactor: Rediseño completo del sistema de permisos"
python create_version.py 2.0.0 "Nuevo sistema de permisos RBAC"
```

## 📊 Ver Historial de Versiones

### En la Web
```
http://127.0.0.1:5000/versiones
```

### Por API
```bash
# Todas las versiones
curl http://127.0.0.1:5000/get_versiones

# Última versión
curl http://127.0.0.1:5000/get_latest_version
```

## 🔄 Flujo de Trabajo Recomendado

```bash
# 1. Hacer cambios en el código
# ... editar archivos ...

# 2. Commit
git add .
git commit -m "feat: Agregar sistema de notificaciones"

# 3. Crear versión
python create_version.py 1.1.0 "Sistema de notificaciones"

# 4. Push a GitHub
git push
```

## 💡 Tips

1. **Versión 0.x.x**: Úsala durante el desarrollo inicial
2. **Versión 1.0.0**: Primera versión estable en producción
3. **Descripción clara**: Usa descripciones que expliquen los cambios
4. **Consistencia**: Mantén un patrón en tus versiones
5. **Documentación**: Actualiza el README con cada versión mayor

## 🎯 Ejemplos Prácticos

### Desarrollo Inicial
```bash
python create_version.py 0.1.0 "Proyecto iniciado"
python create_version.py 0.2.0 "Login y autenticación"
python create_version.py 0.3.0 "CRUD productos"
python create_version.py 0.4.0 "CRUD proveedores"
python create_version.py 0.5.0 "Sistema de facturación"
```

### Primera Versión Estable
```bash
python create_version.py 1.0.0 "Primera versión estable - Lanzamiento"
```

### Mejoras Continuas
```bash
python create_version.py 1.1.0 "Agregar reportes PDF"
python create_version.py 1.2.0 "Dashboard con gráficas"
python create_version.py 1.3.0 "Sistema de notificaciones"
python create_version.py 1.3.1 "Fix: Notificaciones no se mostraban"
```

### Cambio Mayor
```bash
python create_version.py 2.0.0 "Rediseño completo de UI/UX"
```

## 📝 Notas Importantes

- ⚠️ **No uses auto-incremento para versiones importantes** (1.0.0, 2.0.0)
- ✅ **Siempre especifica la versión manualmente** para releases
- 📌 **La versión se muestra en el navbar** de la aplicación
- 🔍 **Todas las versiones quedan registradas** en MongoDB
