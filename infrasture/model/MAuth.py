from pymongo import MongoClient

#* CONEXIÓN A LA BASE DE DATOS
cluster = MongoClient("mongodb://localhost:27017/")
db = cluster["Forporea"]
usuarios = db["usuarios"]

def getUserByEmail(email):
    result = usuarios.find_one({"email": email}, {"email": 1, "password": 1, "rol": 1, "nombre": 1})
    return result

def getAllUsers():
    result = usuarios.find()
    return result
