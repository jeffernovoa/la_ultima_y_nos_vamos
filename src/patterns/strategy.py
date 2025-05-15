class DesempateStrategy:
    def resolver(self, votos):
        raise NotImplementedError()

class AlfabeticoStrategy(DesempateStrategy):
    def resolver(self, votos):
        return sorted(votos)[0]

class AleatorioStrategy(DesempateStrategy):
    import random
    def resolver(self, votos):
        return random.choice(votos)
