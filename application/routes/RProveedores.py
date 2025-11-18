from flask import request, Blueprint, jsonify
import infrasture.model.MProveedores as MProveedores
import domain.VProveedores as VProveedores
from domain.VPermisos import requiere_permiso
from infrasture.jwt_utils import token_required

bp = Blueprint('RProveedores', __name__)



@bp.route('/proveedores', methods=['GET'])
@token_required
def get_proveedores():
    try:
        proveedores_cursor = MProveedores.getAllProveedores()
        proveedores_list = []
        
        for proveedor in proveedores_cursor:
            try:
                proveedores_list.append({
                    '_id': str(proveedor['_id']),
                    'nombre': proveedor.get('nombre', ''),
                    'contacto': proveedor.get('contacto', ''),
                    'telefono': proveedor.get('telefono', ''),
                    'email': proveedor.get('email', ''),
                    'direccion': proveedor.get('direccion', '')
                })
            except Exception as e:
                print(f"Error procesando proveedor: {e}")
                continue
        
        return jsonify({"success": True, "proveedores": proveedores_list})
    except Exception as exc:
        print(f"Error en get_proveedores: {exc}")
        return jsonify({"success": False, "message": "Error al cargar proveedores"}), 500

@bp.route('/proveedores/<proveedor_id>', methods=['GET'])
@token_required
def get_proveedor(proveedor_id):
    try:
        proveedor_data = MProveedores.getProveedorById(proveedor_id)
        validator = VProveedores.getProveedorValidator(proveedor_data=proveedor_data)
        proveedor = validator.validation()
        
        return jsonify({
            "success": True,
            "proveedor": {
                '_id': str(proveedor['_id']),
                'nombre': proveedor.get('nombre', ''),
                'contacto': proveedor.get('contacto', ''),
                'telefono': proveedor.get('telefono', ''),
                'email': proveedor.get('email', ''),
                'direccion': proveedor.get('direccion', '')
            }
        })
    except LookupError as exc:
        return jsonify({"success": False, "message": str(exc)}), 404
    except Exception as exc:
        return jsonify({"success": False, "message": str(exc)}), 500

@bp.route('/proveedores', methods=['POST'])
@token_required
@requiere_permiso('proveedores', 'crear')
def create_proveedor():
    try:
        data = request.get_json(silent=True)
        validator = VProveedores.createProveedorValidator(isJson=request.is_json, payLoad=data)
        proveedor_data = validator.validation()
        
        result = MProveedores.createProveedor(proveedor_data)
        
        return jsonify({
            "success": True,
            "message": "Proveedor creado exitosamente",
            "proveedor_id": str(result.inserted_id)
        }), 201
    except ValueError as exc:
        return jsonify({"success": False, "message": str(exc)}), 400
    except Exception as exc:
        return jsonify({"success": False, "message": str(exc)}), 500

@bp.route('/proveedores/<proveedor_id>', methods=['PUT'])
@token_required
@requiere_permiso('proveedores', 'editar')
def update_proveedor(proveedor_id):
    try:
        data = request.get_json(silent=True)
        validator = VProveedores.updateProveedorValidator(isJson=request.is_json, payLoad=data)
        proveedor_data = validator.validation()
        
        result = MProveedores.updateProveedor(proveedor_id, proveedor_data)
        
        if result.modified_count > 0:
            return jsonify({"success": True, "message": "Proveedor actualizado exitosamente"})
        return jsonify({"success": False, "message": "No se realizaron cambios"}), 404
    except ValueError as exc:
        return jsonify({"success": False, "message": str(exc)}), 400
    except Exception as exc:
        return jsonify({"success": False, "message": str(exc)}), 500

@bp.route('/proveedores/<proveedor_id>', methods=['DELETE'])
@token_required
@requiere_permiso('proveedores', 'eliminar')
def delete_proveedor(proveedor_id):
    try:
        result = MProveedores.deleteProveedor(proveedor_id)
        
        if result.deleted_count > 0:
            return jsonify({"success": True, "message": "Proveedor eliminado exitosamente"})
        return jsonify({"success": False, "message": "Proveedor no encontrado"}), 404
    except Exception as exc:
        return jsonify({"success": False, "message": str(exc)}), 500
