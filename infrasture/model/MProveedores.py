from pymongo import MongoClient
from bson import ObjectId

#* CONEXIÓN A LA BASE DE DATOS
cluster = MongoClient("mongodb://localhost:27017/")
db = cluster["Forporea"]
proveedores = db["proveedores"]

def getAllProveedores():
    result = proveedores.find()
    return result

def getProveedorById(proveedor_id):
    result = proveedores.find_one({"_id": ObjectId(proveedor_id)})
    return result

def createProveedor(proveedor_data):
    result = proveedores.insert_one(proveedor_data)
    return result

def updateProveedor(proveedor_id, proveedor_data):
    result = proveedores.update_one(
        {"_id": ObjectId(proveedor_id)},
        {"$set": proveedor_data}
    )
    return result

def deleteProveedor(proveedor_id):
    result = proveedores.delete_one({"_id": ObjectId(proveedor_id)})
    return result
