from pymongo import MongoClient
from bson import ObjectId

#* CONEXIÓN A LA BASE DE DATOS
cluster = MongoClient("mongodb://localhost:27017/")
db = cluster["Forporea"]
usuarios = db["usuarios"]

def getUserData(user_id):
    result = usuarios.find_one({"_id": ObjectId(user_id)})
    return result
