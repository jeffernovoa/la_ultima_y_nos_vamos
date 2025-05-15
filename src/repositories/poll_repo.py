from src.models.poll import Poll

class PollRepository:
    def __init__(self):
        self.encuestas = {}

    def guardar(self, poll):
        self.encuestas[poll.id] = poll

    def obtener(self, poll_id):
        return self.encuestas.get(poll_id)

    def todas(self):
        return list(self.encuestas.values())