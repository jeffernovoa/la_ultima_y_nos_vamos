from src.models.poll import Poll

class PollFactory:
    @staticmethod
    def crear_encuesta(pregunta, opciones, duracion, tipo="simple"):
        # Aquí puedes devolver subclases según tipo
        return Poll(pregunta, opciones, duracion, tipo)
