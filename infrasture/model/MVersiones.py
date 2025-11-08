from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId

#* CONEXIÓN A LA BASE DE DATOS
cluster = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000, connectTimeoutMS=5000)
db = cluster["Forporea"]
versiones = db["versiones"]

def createVersion(version_data):
    """Crea una nueva versión en la base de datos"""
    version_data['fecha_creacion'] = datetime.now()
    result = versiones.insert_one(version_data)
    return result

def getAllVersiones():
    """Obtiene todas las versiones ordenadas por fecha descendente"""
    try:
        result = versiones.find().sort('fecha_creacion', -1)
        return list(result)
    except Exception as e:
        print(f"Error en getAllVersiones: {e}")
        raise e

def getLatestVersion():
    """Obtiene la última versión registrada"""
    try:
        result = versiones.find_one(sort=[('fecha_creacion', -1)])
        return result
    except Exception as e:
        print(f"Error en getLatestVersion: {e}")
        return None

def getVersionById(version_id):
    """Obtiene una versión específica por ID"""
    result = versiones.find_one({"_id": ObjectId(version_id)})
    return result
