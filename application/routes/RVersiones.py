from flask import Blueprint, render_template, jsonify
from infrasture.model import MVersiones

bp = Blueprint('RVersiones', __name__)

@bp.route('/versiones')
def versiones():
    """Página de historial de versiones"""
    return render_template('Versiones.html')

@bp.route('/get_versiones', methods=['GET'])
def get_versiones():
    """Obtiene todas las versiones"""
    try:
        versiones_cursor = MVersiones.getAllVersiones()
        versiones_list = []
        
        for version in versiones_cursor:
            try:
                versiones_list.append({
                    '_id': str(version['_id']),
                    'version': version.get('version', ''),
                    'descripcion': version.get('descripcion', ''),
                    'commit_hash_short': version.get('commit_hash_short', ''),
                    'commit_message': version.get('commit_message', ''),
                    'autor': version.get('autor', ''),
                    'email': version.get('email', ''),
                    'commit_date': version.get('commit_date', ''),
                    'branch': version.get('branch', ''),
                    'total_archivos': version.get('total_archivos', 0),
                    'fecha_creacion': version.get('fecha_creacion').strftime('%Y-%m-%d %H:%M:%S') if version.get('fecha_creacion') else ''
                })
            except Exception as e:
                print(f"Error procesando versión: {e}")
                continue
        
        return jsonify({"success": True, "versiones": versiones_list})
    except Exception as exc:
        print(f"Error en get_versiones: {exc}")
        return jsonify({"success": False, "message": "Error al cargar versiones"}), 500

@bp.route('/get_version/<version_id>', methods=['GET'])
def get_version(version_id):
    """Obtiene detalles de una versión específica"""
    try:
        version_data = MVersiones.getVersionById(version_id)
        
        if not version_data:
            return jsonify({"success": False, "message": "Versión no encontrada"}), 404
        
        version = {
            '_id': str(version_data['_id']),
            'version': version_data.get('version', ''),
            'descripcion': version_data.get('descripcion', ''),
            'commit_hash': version_data.get('commit_hash', ''),
            'commit_hash_short': version_data.get('commit_hash_short', ''),
            'commit_message': version_data.get('commit_message', ''),
            'autor': version_data.get('autor', ''),
            'email': version_data.get('email', ''),
            'commit_date': version_data.get('commit_date', ''),
            'branch': version_data.get('branch', ''),
            'archivos_modificados': version_data.get('archivos_modificados', []),
            'total_archivos': version_data.get('total_archivos', 0),
            'fecha_creacion': version_data.get('fecha_creacion').strftime('%Y-%m-%d %H:%M:%S') if version_data.get('fecha_creacion') else ''
        }
        
        return jsonify({"success": True, "version": version})
    except Exception as exc:
        print(f"Error en get_version: {exc}")
        return jsonify({"success": False, "message": "Error al cargar versión"}), 500

@bp.route('/get_latest_version', methods=['GET'])
def get_latest_version():
    """Obtiene la última versión registrada"""
    try:
        version_data = MVersiones.getLatestVersion()
        
        if not version_data:
            return jsonify({"success": False, "message": "No hay versiones registradas"}), 404
        
        version = {
            'version': version_data.get('version', ''),
            'commit_hash_short': version_data.get('commit_hash_short', ''),
            'fecha_creacion': version_data.get('fecha_creacion').strftime('%Y-%m-%d %H:%M:%S') if version_data.get('fecha_creacion') else ''
        }
        
        return jsonify({"success": True, "version": version})
    except Exception as exc:
        print(f"Error en get_latest_version: {exc}")
        return jsonify({"success": False, "message": "Error al cargar versión"}), 500
