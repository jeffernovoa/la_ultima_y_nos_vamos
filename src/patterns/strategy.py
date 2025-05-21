import random

class DesempateStrategy:
    def resolve(self, opciones_empate):
        raise NotImplementedError("Subclases deben implementar resolve()")

class AlfabeticoStrategy(DesempateStrategy):
    def resolve(self, opciones_empate):
        return sorted(opciones_empate)[0]

class AleatorioStrategy(DesempateStrategy):
    def resolve(self, opciones_empate):
        return random.choice(opciones_empate)

class ProrrogaStrategy(DesempateStrategy):
    def resolve(self, opciones_empate):
        return "Empate: prórroga necesaria"

def get_desempate_strategy(nombre):
    if nombre == "alfabetico":
        return AlfabeticoStrategy()
    elif nombre == "aleatorio":
        return AleatorioStrategy()
    elif nombre == "prorroga":
        return ProrrogaStrategy()
    else:
        raise ValueError(f"Estrategia '{nombre}' no reconocida")