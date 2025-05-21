from src.repositories.utils.mongo import mongo_db
from datetime import datetime
from src.models.poll import Poll

class EncuestaRepository:
    def __init__(self):
        self.collection = mongo_db["encuestas"]
        self.votos = mongo_db["votos"]

    def guardar_encuesta(self, encuesta: Poll):
        data = encuesta.__dict__.copy()
        data["timestamp_inicio"] = encuesta.timestamp_inicio.isoformat()
        data["timestamp_fin"] = encuesta.timestamp_fin.isoformat()

        existing = self.collection.find_one({"id": encuesta.id})
        if existing:
            self.collection.replace_one({"id": encuesta.id}, data)
        else:
            self.collection.insert_one(data)

    def obtener_encuesta(self, poll_id):
        data = self.collection.find_one({"id": poll_id})
        if not data:
            return None
        return Poll(
            id=data["id"],
            pregunta=data["pregunta"],
            opciones=data["opciones"],
            estado=data["estado"],
            timestamp_inicio=datetime.fromisoformat(data["timestamp_inicio"]),
            timestamp_fin=datetime.fromisoformat(data["timestamp_fin"]),
            tipo=data.get("tipo", "simple")
        )

    def registrar_voto(self, poll_id, username, opcion):
        self.votos.insert_one({
            "poll_id": poll_id,
            "username": username,
            "opcion": opcion,
            "fecha": datetime.utcnow().isoformat()
        })

    def usuario_ya_voto(self, poll_id, username):
        return self.votos.find_one({"poll_id": poll_id, "username": username}) is not None

    def listar_encuestas_activas(self):
        data = self.collection.find({"estado": "activa"})
        encuestas = []
        for d in data:
            encuestas.append(Poll(
                id=d["id"],
                pregunta=d["pregunta"],
                opciones=d["opciones"],
                estado=d["estado"],
                timestamp_inicio=datetime.fromisoformat(d["timestamp_inicio"]),
                timestamp_fin=datetime.fromisoformat(d["timestamp_fin"]),
                tipo=d.get("tipo", "simple")
            ))
        return encuestas
