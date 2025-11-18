from flask import request, Blueprint, jsonify
from bson import ObjectId
import infrasture.model.MProductos as MProductos
import domain.VProductos as VProductos
from domain.VPermisos import requiere_permiso
from infrasture.jwt_utils import token_required

bp = Blueprint('RProductos', __name__)

@bp.route('/productos', methods=['GET'])
@token_required
def get_productos():
    try:
        productos_cursor = MProductos.getAllProductos()
        productos_list = []
        
        for producto in productos_cursor:
            proveedor = MProductos.getProveedorById(producto.get('proveedor_id'))
            productos_list.append({
                '_id': str(producto['_id']),
                'nombre': producto.get('nombre', ''),
                'descripcion': producto.get('descripcion', ''),
                'precio': producto.get('precio', 0),
                'stock': producto.get('stock', 0),
                'proveedor_id': str(producto.get('proveedor_id', '')),
                'proveedor_nombre': proveedor.get('nombre', 'Sin proveedor') if proveedor else 'Sin proveedor'
            })
        
        return jsonify({"success": True, "productos": productos_list})
    except Exception as exc:
        return jsonify({"success": False, "message": str(exc)}), 500

@bp.route('/productos/<producto_id>', methods=['GET'])
@token_required
def get_producto(producto_id):
    try:
        producto_data = MProductos.getProductoById(producto_id)
        validator = VProductos.getProductoValidator(producto_data=producto_data)
        producto = validator.validation()
        
        proveedor = MProductos.getProveedorById(producto.get('proveedor_id'))
        
        return jsonify({
            "success": True,
            "producto": {
                '_id': str(producto['_id']),
                'nombre': producto.get('nombre', ''),
                'descripcion': producto.get('descripcion', ''),
                'precio': producto.get('precio', 0),
                'stock': producto.get('stock', 0),
                'proveedor': {
                    '_id': str(proveedor['_id']) if proveedor else '',
                    'nombre': proveedor.get('nombre', 'Sin proveedor') if proveedor else 'Sin proveedor',
                    'contacto': proveedor.get('contacto', '') if proveedor else '',
                    'telefono': proveedor.get('telefono', '') if proveedor else '',
                    'email': proveedor.get('email', '') if proveedor else '',
                    'direccion': proveedor.get('direccion', '') if proveedor else ''
                }
            }
        })
    except LookupError as exc:
        return jsonify({"success": False, "message": str(exc)}), 404
    except Exception as exc:
        return jsonify({"success": False, "message": str(exc)}), 500

@bp.route('/productos', methods=['POST'])
@token_required
@requiere_permiso('productos', 'crear')
def create_producto():
    try:
        data = request.get_json(silent=True)
        validator = VProductos.createProductoValidator(isJson=request.is_json, payLoad=data)
        producto_data = validator.validation()
        
        result = MProductos.createProducto(producto_data)
        
        return jsonify({
            "success": True,
            "message": "Producto creado exitosamente",
            "producto_id": str(result.inserted_id)
        }), 201
    except ValueError as exc:
        return jsonify({"success": False, "message": str(exc)}), 400
    except Exception as exc:
        return jsonify({"success": False, "message": str(exc)}), 500

@bp.route('/productos/<producto_id>', methods=['PUT'])
@token_required
@requiere_permiso('productos', 'editar')
def update_producto(producto_id):
    try:
        data = request.get_json(silent=True)
        validator = VProductos.updateProductoValidator(isJson=request.is_json, payLoad=data)
        producto_data = validator.validation()
        
        result = MProductos.updateProducto(producto_id, producto_data)
        
        if result.modified_count > 0:
            return jsonify({"success": True, "message": "Producto actualizado exitosamente"})
        return jsonify({"success": False, "message": "No se realizaron cambios"}), 404
    except ValueError as exc:
        return jsonify({"success": False, "message": str(exc)}), 400
    except Exception as exc:
        return jsonify({"success": False, "message": str(exc)}), 500

@bp.route('/productos/<producto_id>', methods=['DELETE'])
@token_required
@requiere_permiso('productos', 'eliminar')
def delete_producto(producto_id):
    try:
        result = MProductos.deleteProducto(producto_id)
        
        if result.deleted_count > 0:
            return jsonify({"success": True, "message": "Producto eliminado exitosamente"})
        return jsonify({"success": False, "message": "Producto no encontrado"}), 404
    except Exception as exc:
        return jsonify({"success": False, "message": str(exc)}), 500
