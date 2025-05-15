import uuid
from datetime import datetime, timedelta
from src.models.vote import Vote

class Poll:
    def __init__(self, pregunta, opciones, duracion):
        self.id = str(uuid.uuid4())
        self.pregunta = pregunta
        self.opciones = opciones
        self.votos = []
        self.estado = "activa"
        self.timestamp_inicio = datetime.now()
        self.duracion = timedelta(seconds=duracion)

    def agregar_voto(self, voto):
        self.votos.append(voto)

    def esta_activa(self):
        return self.estado == "activa" and datetime.now() < self.timestamp_inicio + self.duracion

    def cerrar(self):
        self.estado = "cerrada"

    def resultados(self):
        conteo = {op: 0 for op in self.opciones}
        for v in self.votos:
            conteo[v.opcion] += 1
        return conteo
