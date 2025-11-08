from flask import render_template, Blueprint, session, jsonify
import infrasture.model.MInicio as MInicio
import infrasture.model.MVersiones as MVersiones
from domain.VPermisos import obtener_permisos_usuario

bp = Blueprint('RInicio', __name__)

@bp.route('/inicio')
def inicio():
    return render_template('Inicio.html', active_page='inicio')

@bp.route('/get_user_info', methods=['GET'])
def get_user_info():
    try:
        user_id = session.get('user_id')
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
