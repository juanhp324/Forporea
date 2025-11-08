from bson import ObjectId
import time
from infrasture.db import db

#* COLECCIÓN DE PROVEEDORES
proveedores = db["proveedores"]

def getAllProveedores():
    max_retries = 3
    retry_delay = 0.5  # 500ms
    
    for attempt in range(max_retries):
        try:
            result = proveedores.find()
            return list(result)
        except Exception as e:
            print(f"Error en getAllProveedores (intento {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
            else:
                raise e

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
