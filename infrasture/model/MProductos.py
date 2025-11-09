from bson import ObjectId
from infrasture.db import get_database

def _get_productos_collection():
    """Obtiene la colección de productos con conexión activa"""
    db = get_database()
    return db["productos"]

def _get_proveedores_collection():
    """Obtiene la colección de proveedores con conexión activa"""
    db = get_database()
    return db["proveedores"]

def getAllProductos():
    productos = _get_productos_collection()
    cursor = productos.find().sort("_id", -1)  # -1 para orden descendente (más reciente primero)
    result = list(cursor)
    cursor.close()
    return result

def getProductoById(producto_id):
    productos = _get_productos_collection()
    result = productos.find_one({"_id": ObjectId(producto_id)})
    return result

def createProducto(producto_data):
    productos = _get_productos_collection()
    result = productos.insert_one(producto_data)
    return result

def updateProducto(producto_id, producto_data):
    productos = _get_productos_collection()
    result = productos.update_one(
        {"_id": ObjectId(producto_id)},
        {"$set": producto_data}
    )
    return result

def deleteProducto(producto_id):
    productos = _get_productos_collection()
    result = productos.delete_one({"_id": ObjectId(producto_id)})
    return result

def getProveedorById(proveedor_id):
    proveedores = _get_proveedores_collection()
    result = proveedores.find_one({"_id": ObjectId(proveedor_id)})
    return result


