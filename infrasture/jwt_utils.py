import jwt
from datetime import datetime, timezone
from functools import wraps
from flask import request, jsonify
from config import Config       

def generate_access_token(user_id, email, rol, nombre):
    payload = {
        'user_id': user_id,
        'email': email,
        'rol': rol,
        'nombre': nombre,
        'exp': datetime.now(timezone.utc) + Config.JWT_ACCESS_TOKEN_EXPIRES,  # Expira en 1 hora
        'iat': datetime.now(timezone.utc)  # Fecha de emisión
    }
    return jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm='HS256')

def generate_refresh_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.now(timezone.utc) + Config.JWT_REFRESH_TOKEN_EXPIRES, # Expira en 30 dias
        'iat': datetime.now(timezone.utc) # Fecha de emisión
    }
    return jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm='HS256')

def get_current_user():
    """Obtiene el usuario actual del token JWT"""
    return getattr(request, 'current_user', None)
    
def decode_token(token):
    try:
        payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError('Token expirado')
    except jwt.InvalidTokenError:
        raise ValueError('Token inválido')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Extraer token del header: Authorization: Bearer eyJhbGci...
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            token = auth_header.split(' ')[1]  # Obtener la parte después de "Bearer "
        
        if not token:
            return jsonify({'message': 'Token no proporcionado'}), 401
        
        try:
            payload = decode_token(token)
            request.current_user = payload  # Guardar datos del usuario en el request
        except ValueError as e:
            return jsonify({'message': str(e)}), 401
        
        return f(*args, **kwargs)
    
    return decorated