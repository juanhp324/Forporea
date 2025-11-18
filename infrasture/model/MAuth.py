from infrasture.db import get_database

def _get_usuarios_collection():
    """Obtiene la colección de usuarios con conexión activa"""
    db = get_database()
    return db["usuarios"]

def getUserByEmail(email):
    usuarios = _get_usuarios_collection()
    result = usuarios.find_one({"email": email}, {"email": 1, "password": 1, "rol": 1, "nombre": 1, "user": 1})
    return result

def getUserById(user_id):

    from bson import ObjectId
    usuarios = _get_usuarios_collection()
    result = usuarios.find_one({"_id": ObjectId(user_id)}, {"email": 1, "password": 1, "rol": 1, "nombre": 1, "user": 1})
    return result

def getAllUsers():
    usuarios = _get_usuarios_collection()
    cursor = usuarios.find()
    result = list(cursor)
    cursor.close()
    return result
