from bson import ObjectId
from infrasture.db import get_database

def _get_facturas_collection():
    """Obtiene la colección de facturas con conexión activa"""
    db = get_database()
    return db["facturas"]

def _get_productos_collection():
    """Obtiene la colección de productos con conexión activa"""
    db = get_database()
    return db["productos"]

def getAllFacturas():
    facturas = _get_facturas_collection()
    cursor = facturas.find()
    result = list(cursor)
    cursor.close()
    return result

def getFacturaById(factura_id):
    facturas = _get_facturas_collection()
    result = facturas.find_one({"_id": ObjectId(factura_id)})
    return result

def createFactura(factura_data):
    facturas = _get_facturas_collection()
    result = facturas.insert_one(factura_data)
    return result

def getProductoById(producto_id):
    productos = _get_productos_collection()
    result = productos.find_one({"_id": ObjectId(producto_id)})
    return result

def getAllProductos():
    productos = _get_productos_collection()
    cursor = productos.find()
    result = list(cursor)
    cursor.close()
    return result

def updateProductoStock(producto_id, nuevo_stock):
    productos = _get_productos_collection()
    result = productos.update_one(
        {"_id": ObjectId(producto_id)},
        {"$set": {"stock": nuevo_stock}}
    )
    return result
