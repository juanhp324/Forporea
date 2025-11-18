from flask import request, Blueprint, jsonify
import infrasture.model.MAuth as MAuth
import infrasture.model.MVersiones as MVersiones
import domain.VAuth as VAuth
from infrasture.jwt_utils import generate_access_token, generate_refresh_token, decode_token
bp = Blueprint('RAuth', __name__)


@bp.route('/Login', methods=['POST'])
def Login():
    data = request.get_json(silent=True)
    login = VAuth.loginValidator(is_json=request.is_json, payLoad=data)

    try:
        userData = login.validation()
    except ValueError as exc:
        return jsonify({"message": str(exc)}), 400
    except LookupError as exc:
        return jsonify({"message": str(exc)}), 404
    except PermissionError as exc:
        return jsonify({"message": str(exc)}), 401

    access_token = generate_access_token(
        user_id=str(userData['_id']),
        email=userData['email'],
        rol=userData.get('rol', 'usuario'),
        nombre=userData.get('nombre', 'Usuario')
    )
    
    refresh_token = generate_refresh_token(str(userData['_id']))

    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": {
            "id": str(userData['_id']),
            "email": userData['email'],
            "rol": userData.get('rol'),
            "nombre": userData.get('nombre')
        }
    }), 200

@bp.route('/logout')
def logout():
    return jsonify({
        "success": True,
        "message": "Sesión cerrada exitosamente"
    }), 200

@bp.route('/refresh', methods=['POST'])
def refresh():
    """Renueva el access token usando el refresh token"""
    data = request.get_json(silent=True)
    refresh_token = data.get('refresh_token')
    
    if not refresh_token:
        return jsonify({"message": "Refresh token no proporcionado"}), 401
    
    try:

        payload = decode_token(refresh_token)
        user_id = payload['user_id']
        
        # Obtener datos actualizados del usuario
        user_data = MAuth.getUserById(user_id)
        if not user_data:
            return jsonify({"message": "Usuario no encontrado"}), 404
        
        # Generar nuevo access token
        new_access_token = generate_access_token(
            user_id=str(user_data['_id']),
            email=user_data['email'],
            rol=user_data.get('rol', 'usuario'),
            nombre=user_data.get('nombre', 'Usuario')
        )
        
        return jsonify({
            "success": True,
            "access_token": new_access_token
        }), 200
        
    except ValueError as e:
        return jsonify({"message": str(e)}), 401

@bp.route('/get_latest_version', methods=['GET'])
def get_latest_version():
    """Obtiene la última versión registrada (endpoint público)"""
    try:
        version_data = MVersiones.getLatestVersion()
        
        if not version_data:
            return jsonify({"success": True, "version": {"version": "0.0.0"}})
        
        version = {
            'version': version_data.get('version', '0.0.0')
        }
        
        return jsonify({"success": True, "version": version})
    except Exception as exc:
        return jsonify({"success": False, "message": str(exc)}), 500
