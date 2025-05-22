from datetime import datetime, timedelta

class Poll:
    def __init__(self, poll_id, pregunta, opciones, duracion_segundos):
        self.id = poll_id
        self.pregunta = pregunta
        self.opciones = opciones
        self.votos = {}  # username: opcion/es
        self.estado = "activa"
        self.timestamp_inicio = datetime.utcnow()
        self.duracion = timedelta(seconds=duracion_segundos)

    def esta_activa(self):
        return self.estado == "activa" and datetime.utcnow() < self.timestamp_inicio + self.duracion

    def cerrar(self):
        self.estado = "cerrada"

    def contar_votos(self):
        conteo = {op: 0 for op in self.opciones}
        for votos in self.votos.values():
            if isinstance(votos, list):
                for v in votos:
                    conteo[v] += 1
            else:
                conteo[votos] += 1
        return conteo

    def registrar_voto(self, username, voto):
        if username in self.votos:
            raise ValueError("El usuario ya ha votado.")
        self.votos[username] = voto


class SimplePoll(Poll):
    def registrar_voto(self, username, voto):
        if voto not in self.opciones:
            raise ValueError("Opción no válida.")
        super().registrar_voto(username, voto)


class MultiplePoll(Poll):
    def registrar_voto(self, username, votos):
        if not isinstance(votos, list):
            raise ValueError("Se esperaban múltiples opciones.")
        for voto in votos:
            if voto not in self.opciones:
                raise ValueError("Opción no válida.")
        super().registrar_voto(username, votos)


class WeightedPoll(Poll):
    def registrar_voto(self, username, votos_ponderados):
        # votos_ponderados: dict opcion -> peso
        if not isinstance(votos_ponderados, dict):
            raise ValueError("Formato inválido.")
        for opcion, peso in votos_ponderados.items():
            if opcion not in self.opciones or not isinstance(peso, int):
                raise ValueError("Opción no válida o peso no entero.")
        super().registrar_voto(username, votos_ponderados)

    def contar_votos(self):
        conteo = {op: 0 for op in self.opciones}
        for votos in self.votos.values():
            for opcion, peso in votos.items():
                conteo[opcion] += peso
        return conteo
