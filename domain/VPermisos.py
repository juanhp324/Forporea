from flask import session, jsonify
from functools import wraps

# Definición de permisos por rol
PERMISOS = {
    'admin': {
        'productos': ['ver', 'crear', 'editar', 'eliminar'],
        'proveedores': ['ver', 'crear', 'editar', 'eliminar'],
        'facturacion': ['ver', 'crear']
    },
    'user': {
        'productos': ['ver'],
        'proveedores': ['ver'],
        'facturacion': ['ver', 'crear']
    }
}

def tiene_permiso(modulo, accion):
    """
    Verifica si el usuario actual tiene permiso para realizar una acción en un módulo
    """
    rol = session.get('rol', 'user')
    permisos_rol = PERMISOS.get(rol, {})
    permisos_modulo = permisos_rol.get(modulo, [])
    return accion in permisos_modulo

def requiere_permiso(modulo, accion):
    """
    Decorador para proteger rutas que requieren permisos específicos
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not tiene_permiso(modulo, accion):
                return jsonify({
                    "success": False,
                    "message": "No tienes permisos para realizar esta acción"
                }), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def obtener_permisos_usuario():
    """
    Obtiene todos los permisos del usuario actual
    """
    rol = session.get('rol', 'user')
    return PERMISOS.get(rol, {})
