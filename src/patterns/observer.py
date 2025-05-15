class Observer:
    def update(self, poll_id):
        raise NotImplementedError()

class Observable:
    def __init__(self):
        self._observadores = []

    def registrar(self, obs: Observer):
        self._observadores.append(obs)

    def notificar(self, poll_id):
        for obs in self._observadores:
            obs.update(poll_id)
