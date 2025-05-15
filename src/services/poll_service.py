from src.models.poll import Poll
from src.models.vote import Vote
from src.services.observer import Observer

class PollService:
    def __init__(self, repo):
        self.repo = repo
        self.observers = []

    def register_observer(self, observer: Observer):
        self.observers.append(observer)

    def notify_observers(self, poll):
        for obs in self.observers:
            obs.update(poll)

    def crear_encuesta(self, pregunta, opciones, duracion):
        poll = Poll(pregunta, opciones, duracion)
        self.repo.guardar(poll)
        return poll.id

    def votar(self, poll_id, username, opcion):
        poll = self.repo.obtener(poll_id)
        if not poll:
            raise Exception("Encuesta no existe")
        if not poll.esta_activa():
            raise Exception("Encuesta cerrada")
        if any(v.username == username for v in poll.votos):
            raise Exception("Usuario ya votó")
        voto = Vote(username, opcion)
        poll.agregar_voto(voto)

    def cerrar_encuesta(self, poll_id):
        poll = self.repo.obtener(poll_id)
        if poll and poll.estado == "activa":
            poll.cerrar()
            self.notify_observers(poll)

    def verificar_cierres(self):
        for poll in self.repo.todas():
            if poll.esta_activa() is False and poll.estado == "activa":
                poll.cerrar()
                self.notify_observers(poll)

    def resultados_finales(self, poll_id):
        poll = self.repo.obtener(poll_id)
        if poll.estado != "cerrada":
            raise Exception("Encuesta no cerrada")
        return poll.resultados()

    def resultados_parciales(self, poll_id):
        poll = self.repo.obtener(poll_id)
        if poll.estado != "activa":
            raise Exception("Encuesta no activa")
        return poll.resultados()