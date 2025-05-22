import random
import json

# === Desempate ===

class DesempateStrategy:
    def resolver(self, opciones_con_empate):
        raise NotImplementedError

class DesempateAlfabetico(DesempateStrategy):
    def resolver(self, opciones_con_empate):
        return sorted(opciones_con_empate)[0]

class DesempateAleatorio(DesempateStrategy):
    def resolver(self, opciones_con_empate):
        return random.choice(opciones_con_empate)

class DesempateProrroga(DesempateStrategy):
    def resolver(self, opciones_con_empate):
        return None  # Indica que se debe extender la encuesta

# === Presentación de resultados ===

class FormatoResultadosStrategy:
    def formatear(self, resultados_dict):
        raise NotImplementedError

class FormatoTextoPlano(FormatoResultadosStrategy):
    def formatear(self, resultados_dict):
        return "\n".join(f"{op}: {votos} votos" for op, votos in resultados_dict.items())

class FormatoAsciiGrafico(FormatoResultadosStrategy):
    def formatear(self, resultados_dict):
        return "\n".join(f"{op}: {'█' * votos} ({votos})" for op, votos in resultados_dict.items())

class FormatoJSON(FormatoResultadosStrategy):
    def formatear(self, resultados_dict):
        return json.dumps(resultados_dict, indent=2)
