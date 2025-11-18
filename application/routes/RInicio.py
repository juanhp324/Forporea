from flask import Blueprint, jsonify
import infrasture.model.MInicio as MInicio
import infrasture.model.MVersiones as MVersiones
from domain.VPermisos import obtener_permisos_usuario
from infrasture.jwt_utils import token_required, get_current_user

bp = Blueprint('RInicio', __name__)

@bp.route('/user-info', methods=['GET'])
@token_required
def get_user_info():
    try:
        current_user = get_current_user()
        user_id = current_user.get('user_id')
        user_data = MInicio.getUserData(user_id)
        
        if not user_data:
            return jsonify({"success": False, "message": "Usuario no encontrado"}), 404
        
        permisos = obtener_permisos_usuario()
        
        # Obtener última versión
        latest_version = MVersiones.getLatestVersion()
        version_info = {
            'version': latest_version.get('version', '0.0.0') if latest_version else '0.0.0'
        }
        
        return jsonify({
            "success": True,
            "nombre": user_data.get('nombre', 'Usuario'),
            "email": user_data.get('email', ''),
            "user": user_data.get('user', ''),
            "rol": user_data.get('rol', 'usuario'),
            "permisos": permisos,
            "version": version_info
        })
    except Exception as exc:
        return jsonify({"success": False, "message": str(exc)}), 500
