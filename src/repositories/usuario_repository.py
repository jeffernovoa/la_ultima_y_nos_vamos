from src.databases.mongo_connection import MongoConnection

mongo = MongoConnection()
usuarios = mongo.get_collection("usuarios")

def crear_usuario(username, email):
    if usuarios.find_one({"username": username}):
        raise ValueError("Usuario ya existe")
    usuarios.insert_one({
        "username": username,
        "email": email,
        "nfts": [],
        "votos": []
    })
