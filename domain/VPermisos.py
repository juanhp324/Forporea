from flask import jsonify
from functools import wraps
from infrasture.jwt_utils import get_current_user

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

    current_user = get_current_user()

    if not current_user:
        return False
    
    rol = current_user.get('rol', 'user')
    permisos_rol = PERMISOS.get(rol, {})
    permisos_modulo = permisos_rol.get(modulo, [])
    return accion in permisos_modulo

def requiere_permiso(modulo, accion):
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
    current_user = get_current_user()
    
    if not current_user:
        return {}
    
    rol = current_user.get('rol', 'user')
    return PERMISOS.get(rol, {})
