from infrasture.db import db

#* COLECCIÓN DE USUARIOS
usuarios = db["usuarios"]

def getUserByEmail(email):
    result = usuarios.find_one({"email": email}, {"email": 1, "password": 1, "rol": 1, "nombre": 1, "user": 1})
    return result

def getAllUsers():
    result = usuarios.find()
    return result
