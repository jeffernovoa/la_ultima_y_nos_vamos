import uuid
from datetime import datetime, timedelta
from src.models.poll import Poll
from src.repositories.poll_repository import PollRepository
from src.patterns.observer import Observable

# Importar estrategias
from src.patterns.strategy import (
    DesempateStrategy,
    DesempateAlfabetico,
    FormatoResultadosStrategy,
    FormatoTextoPlano
)

class PollService(Observable):
    def __init__(
        self,
        encuesta_repo: PollRepository,
        estrategia_desempate: DesempateStrategy = DesempateAlfabetico(),
        estrategia_formato: FormatoResultadosStrategy = FormatoTextoPlano()
    ):
        super().__init__()
        self.repo = encuesta_repo
        self.estrategia_desempate = estrategia_desempate
        self.estrategia_formato = estrategia_formato

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
                if op not in encuesta.opciones:
                    raise Exception(f"Opción inválida: {op}")
                encuesta.opciones[op] += 1
        else:
            if opcion not in encuesta.opciones:
                raise Exception(f"Opción inválida: {opcion}")
            encuesta.opciones[opcion] += 1

        self.repo.registrar_voto(poll_id, username, opcion)
        self.repo.guardar_encuesta(encuesta)

        if datetime.utcnow() > encuesta.timestamp_fin:
            self.close_poll(poll_id)

        return True

    def close_poll(self, poll_id):
        encuesta = self.repo.obtener_encuesta(poll_id)
        if not encuesta or encuesta.estado == "cerrada":
            return

        encuesta.estado = "cerrada"
        self.repo.guardar_encuesta(encuesta)
        self.notify_observers(encuesta)

    def get_partial_results(self, poll_id):
        encuesta = self.repo.obtener_encuesta(poll_id)
        if not encuesta:
            raise Exception("Encuesta no encontrada")

        total = sum(encuesta.opciones.values())
        resultados = {
            opcion: {
                "votos": count,
                "porcentaje": (count / total * 100) if total > 0 else 0
            }
            for opcion, count in encuesta.opciones.items()
        }

        return resultados

    def get_final_results(self, poll_id):
        encuesta = self.repo.obtener_encuesta(poll_id)
        if not encuesta or encuesta.estado != "cerrada":
            raise Exception("Encuesta aún no cerrada")

        resultados = self.get_partial_results(poll_id)
        votos_por_opcion = {op: datos["votos"] for op, datos in resultados.items()}

        max_votos = max(votos_por_opcion.values())
        ganadores = [op for op, votos in votos_por_opcion.items() if votos == max_votos]

        resultado_final = dict(votos_por_opcion)

        if len(ganadores) > 1:
            elegido = self.estrategia_desempate.resolver(ganadores)
            if elegido is None:
                resultado_final["desempate"] = f"Empate entre: {', '.join(ganadores)} (requiere prórroga)"
            else:
                resultado_final["desempate"] = f"Ganador tras desempate: {elegido}"
        else:
            resultado_final["ganador"] = ganadores[0]

        return self.estrategia_formato.formatear(resultado_final)

    def check_and_close_expired(self):
        encuestas = self.repo.listar_encuestas_activas()
        for encuesta in encuestas:
            if datetime.utcnow() > encuesta.timestamp_fin:
                self.close_poll(encuesta.id)
