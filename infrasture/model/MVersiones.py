from datetime import datetime
from bson import ObjectId
from infrasture.db import get_database

def _get_versiones_collection():
    """Obtiene la colección de versiones con conexión activa"""
    db = get_database()
    return db["versiones"]

def createVersion(version_data):
    """Crea una nueva versión en la base de datos"""
    versiones = _get_versiones_collection()
    version_data['fecha_creacion'] = datetime.now()
    result = versiones.insert_one(version_data)
    return result

def getAllVersiones():
    """Obtiene todas las versiones ordenadas por fecha descendente"""
    try:
        versiones = _get_versiones_collection()
        cursor = versiones.find().sort('fecha_creacion', -1)
        result = list(cursor)
        cursor.close()
        return result
    except Exception as e:
        print(f"Error en getAllVersiones: {e}")
        raise e

def getLatestVersion():
    """Obtiene la última versión registrada"""
    try:
        versiones = _get_versiones_collection()
        result = versiones.find_one(sort=[('fecha_creacion', -1)])
        return result
    except Exception as e:
        print(f"Error en getLatestVersion: {e}")
        return None

def getVersionById(version_id):
    """Obtiene una versión específica por ID"""
    versiones = _get_versiones_collection()
    result = versiones.find_one({"_id": ObjectId(version_id)})
    return result
