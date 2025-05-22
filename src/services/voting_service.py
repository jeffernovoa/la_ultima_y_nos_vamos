import uuid
from datetime import datetime
from src.databases.mongo_connection import MongoConnection
from src.databases.neo4j_connection import Neo4jConnection

class VotingService:
    def __init__(self):
        self.mongo = MongoConnection()
        self.neo4j = Neo4jConnection()
        self.usuarios = self.mongo.get_collection("usuarios")
        self.encuestas = self.mongo.get_collection("encuestas")
        self.tokens = self.mongo.get_collection("tokens")

    def votar(self, username: str, poll_id: str, opcion: str):
        # Validación: Usuario
        user = self.usuarios.find_one({"username": username})
        if not user:
            raise ValueError("Usuario no encontrado.")

        # Validación: Encuesta y opción
        encuesta = self.encuestas.find_one({"poll_id": poll_id, "estado": "activa"})
        if not encuesta or opcion not in encuesta["opciones"]:
            raise ValueError("Encuesta no encontrada o opción inválida.")

        # Verificar si ya votó
        if poll_id in user.get("votos", []):
            raise ValueError("El usuario ya votó en esta encuesta.")

        # 1. Guardar voto en MongoDB
        self.usuarios.update_one(
            {"username": username},
            {"$push": {"votos": poll_id}}
        )

        # 2. Relación en Neo4j
        self.neo4j.query("""
            MERGE (u:Usuario {username: $username})
            MERGE (e:Encuesta {id: $poll_id})
            MERGE (u)-[:VOTO {opcion: $opcion}]->(e)
        """, {
            "username": username,
            "poll_id": poll_id,
            "opcion": opcion
        })

        # 3. Generar Token NFT simulado
        token_id = str(uuid.uuid4())
        token = {
            "token_id": token_id,
            "owner": username,
            "poll_id": poll_id,
            "opcion": opcion,
            "issued_at": datetime.utcnow().isoformat()
        }
        self.tokens.insert_one(token)

        # Asignar token al usuario
        self.usuarios.update_one(
            {"username": username},
            {"$push": {"nfts": token_id}}
        )

        return token
