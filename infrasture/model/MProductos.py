from pymongo import MongoClient
from bson import ObjectId

#* CONEXIÓN A LA BASE DE DATOS
cluster = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000, connectTimeoutMS=5000)
db = cluster["Forporea"]
productos = db["productos"]
proveedores = db["proveedores"]

def getAllProductos():
    result = productos.find()
    return result

def getProductoById(producto_id):
    result = productos.find_one({"_id": ObjectId(producto_id)})
    return result

def createProducto(producto_data):
    result = productos.insert_one(producto_data)
    return result

def updateProducto(producto_id, producto_data):
    result = productos.update_one(
        {"_id": ObjectId(producto_id)},
        {"$set": producto_data}
    )
    return result

def deleteProducto(producto_id):
    result = productos.delete_one({"_id": ObjectId(producto_id)})
    return result

def getProveedorById(proveedor_id):
    result = proveedores.find_one({"_id": ObjectId(proveedor_id)})
    return result


