from bson import ObjectId
from infrasture.db import get_database

def _get_usuarios_collection():
    """Obtiene la colección de usuarios con conexión activa"""
    db = get_database()
    return db["usuarios"]

def getUserData(user_id):
    usuarios = _get_usuarios_collection()
    result = usuarios.find_one({"_id": ObjectId(user_id)})
    return result
