from bson import ObjectId
import time
from infrasture.db import get_database

def _get_collection():
    """Obtiene la colección de proveedores con conexión activa"""
    db = get_database()
    return db["proveedores"]

def getAllProveedores():
    max_retries = 3
    retry_delay = 0.5  # 500ms
    
    for attempt in range(max_retries):
        try:
            # Obtener colección con conexión activa
            proveedores = _get_collection()
            # Obtener cursor y convertir a lista inmediatamente
            cursor = proveedores.find()
            result = list(cursor)
            # Cerrar el cursor explícitamente
            cursor.close()
            return result
        except Exception as e:
            print(f"Error en getAllProveedores (intento {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
            else:
                raise e

def getProveedorById(proveedor_id):
    proveedores = _get_collection()
    result = proveedores.find_one({"_id": ObjectId(proveedor_id)})
    return result

def createProveedor(proveedor_data):
    proveedores = _get_collection()
    result = proveedores.insert_one(proveedor_data)
    return result

def updateProveedor(proveedor_id, proveedor_data):
    proveedores = _get_collection()
    result = proveedores.update_one(
        {"_id": ObjectId(proveedor_id)},
        {"$set": proveedor_data}
    )
    return result

def deleteProveedor(proveedor_id):
    proveedores = _get_collection()
    result = proveedores.delete_one({"_id": ObjectId(proveedor_id)})
    return result
