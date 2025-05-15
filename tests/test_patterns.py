from datetime import datetime
import uuid

class Poll:
    def __init__(self, pregunta, opciones, duracion_segundos, tipo="simple"):
        self.id = str(uuid.uuid4())
        self.pregunta = pregunta
        self.opciones = opciones
        self.votos = {op: [] for op in opciones}
        self.estado = "activa"
        self.timestamp_inicio = datetime.now()
        self.duracion = duracion_segundos
        self.tipo = tipo

    def agregar_voto(self, username, opcion):
        if opcion in self.opciones and username not in sum(self.votos.values(), []):
            self.votos[opcion].append(username)

    def cerrar(self):
        self.estado = "cerrada"
