from transformers import pipeline

class ChatbotService:
    def __init__(self, poll_service):
        self.poll_service = poll_service
        self.pipeline = pipeline("text-generation", model="gpt2")

    def responder(self, username, mensaje):
        mensaje_lower = mensaje.lower()

        if "quién va ganando" in mensaje_lower:
            return self._respuesta_ganador()
        elif "cuánto falta" in mensaje_lower:
            return self._respuesta_tiempo()
        else:
            respuesta = self.pipeline(mensaje, max_length=50, num_return_sequences=1)
            return respuesta[0]["generated_text"]

    def _respuesta_ganador(self):
        encuestas = self.poll_service.repo.listar_encuestas_activas()
        if not encuestas:
            return "No hay encuestas activas."
        encuesta = encuestas[0]
        resultados = self.poll_service.get_partial_results(encuesta.id)
        top = max(resultados.items(), key=lambda x: x[1]["votos"])
        return f"En la encuesta '{encuesta.pregunta}', va ganando '{top[0]}' con {top[1]['votos']} votos."

    def _respuesta_tiempo(self):
        encuestas = self.poll_service.repo.listar_encuestas_activas()
        if not encuestas:
            return "No hay encuestas activas."
        encuesta = encuestas[0]
        falta = (encuesta.timestamp_fin - encuesta.timestamp_inicio).total_seconds()
        return f"A la encuesta le quedan {int(falta)} segundos."
