from bson import ObjectId
from infrasture.db import db

#* COLECCIÓN DE USUARIOS
usuarios = db["usuarios"]

def getUserData(user_id):
    result = usuarios.find_one({"_id": ObjectId(user_id)})
    return result
