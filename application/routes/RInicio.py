from flask import render_template, Blueprint, session, jsonify
import infrasture.model.MInicio as MInicio

bp = Blueprint('RInicio', __name__)

@bp.route('/inicio')
def inicio():
    return render_template('Inicio.html')

@bp.route('/get_user_info', methods=['GET'])
def get_user_info():
    try:
        user_id = session.get('user_id')
        user_data = MInicio.getUserData(user_id)
        
        if not user_data:
            return jsonify({"success": False, "message": "Usuario no encontrado"}), 404
        
        return jsonify({
            "success": True,
            "nombre": user_data.get('nombre', 'Usuario'),
            "email": user_data.get('email', ''),
            "rol": user_data.get('rol', 'usuario')
        })
    except Exception as exc:
        return jsonify({"success": False, "message": str(exc)}), 500
