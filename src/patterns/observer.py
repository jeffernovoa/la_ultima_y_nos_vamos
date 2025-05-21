class Observer:
    def update(self, _):
        raise NotImplementedError("Subclases deben implementar update()")


class Observable:
    def __init__(self):
        self._observers = []

    def add_observer(self, observer: Observer):
        self._observers.append(observer)

    def remove_observer(self, observer: Observer):
        self._observers.remove(observer)

    def notify_observers(self, encuesta):
        for observer in self._observers:
            observer.update(encuesta)