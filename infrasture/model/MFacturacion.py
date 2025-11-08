from bson import ObjectId
from infrasture.db import db

#* COLECCIONES
facturas = db["facturas"]
productos = db["productos"]

def getAllFacturas():
    result = facturas.find()
    return result

def getFacturaById(factura_id):
    result = facturas.find_one({"_id": ObjectId(factura_id)})
    return result

def createFactura(factura_data):
    result = facturas.insert_one(factura_data)
    return result

def getProductoById(producto_id):
    result = productos.find_one({"_id": ObjectId(producto_id)})
    return result

def getAllProductos():
    result = productos.find()
    return result

def updateProductoStock(producto_id, nuevo_stock):
    result = productos.update_one(
        {"_id": ObjectId(producto_id)},
        {"$set": {"stock": nuevo_stock}}
    )
    return result
