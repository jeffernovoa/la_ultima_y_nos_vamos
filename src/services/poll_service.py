import uuid
from datetime import datetime, timedelta
from src.models.poll import Poll
from src.repositories.encuesta_repository import EncuestaRepository
from src.patterns.observer import Observable
from src.patterns.strategy import get_desempate_strategy

class PollService(Observable):
    def __init__(self, encuesta_repo: EncuestaRepository):
        super().__init__()
        self.repo = encuesta_repo

    def create_poll(self, pregunta, opciones, duracion_segundos, tipo="simple"):
        poll_id = str(uuid.uuid4())
        inicio = datetime.utcnow()
        fin = inicio + timedelta(seconds=duracion_segundos)
        nueva = Poll(
            id=poll_id,
            pregunta=pregunta,
            opciones={op: 0 for op in opciones},
            estado="activa",
            timestamp_inicio=inicio,
            timestamp_fin=fin,
            tipo=tipo
        )
        self.repo.guardar_encuesta(nueva)
        return poll_id

    def vote(self, poll_id, username, opcion):
        encuesta = self.repo.obtener_encuesta(poll_id)

        if not encuesta or encuesta.estado != "activa":
            raise Exception("Encuesta no activa o no encontrada")

        if self.repo.usuario_ya_voto(poll_id, username):
            raise Exception("Usuario ya votó")

        if isinstance(opcion, list):
            for op in opcion:
                encuesta.opciones[op] += 1
        else:
            encuesta.opciones[opcion] += 1

        self.repo.registrar_voto(poll_id, username, opcion)
        self.repo.guardar_encuesta(encuesta)

        if datetime.utcnow() > encuesta.timestamp_fin:
            self.close_poll(poll_id)

    def close_poll(self, poll_id):
        encuesta = self.repo.obtener_encuesta(poll_id)
        if encuesta.estado == "cerrada":
            return

        encuesta.estado = "cerrada"
        self.repo.guardar_encuesta(encuesta)
        self.notify_observers(encuesta)

    def get_partial_results(self, poll_id):
        encuesta = self.repo.obtener_encuesta(poll_id)
        total = sum(encuesta.opciones.values())
        return {
            opcion: {
                "votos": count,
                "porcentaje": (count / total * 100) if total > 0 else 0
            }
            for opcion, count in encuesta.opciones.items()
        }

    def get_final_results(self, poll_id):
        encuesta = self.repo.obtener_encuesta(poll_id)
        if encuesta.estado != "cerrada":
            raise Exception("Encuesta aún no cerrada")

        resultados = self.get_partial_results(poll_id)
        max_votos = max(op["votos"] for op in resultados.values())
        ganadores = [op for op, datos in resultados.items() if datos["votos"] == max_votos]

        if len(ganadores) > 1:
            strategy = get_desempate_strategy("alfabetico")  # Puedes hacerlo dinámico
            elegido = strategy.resolve(ganadores)
            resultados["desempate"] = elegido
        return resultados

    def check_and_close_expired(self):
        encuestas = self.repo.listar_encuestas_activas()
        for encuesta in encuestas:
            if datetime.utcnow() > encuesta.timestamp_fin:
                self.close_poll(encuesta.id)
