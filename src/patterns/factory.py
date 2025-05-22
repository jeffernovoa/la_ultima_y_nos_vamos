from src.models.poll import Poll, SimplePoll, MultiplePoll, WeightedPoll
from src.models.token_nft import TokenNFT, StandardToken, LimitedEditionToken
import uuid
from datetime import datetime

class PollFactory:
    @staticmethod
    def create_poll(tipo, pregunta, opciones, duracion):
        poll_id = str(uuid.uuid4())
        if tipo == "simple":
            return SimplePoll(poll_id, pregunta, opciones, duracion)
        elif tipo == "multiple":
            return MultiplePoll(poll_id, pregunta, opciones, duracion)
        elif tipo == "ponderada":
            return WeightedPoll(poll_id, pregunta, opciones, duracion)
        else:
            raise ValueError(f"Tipo de encuesta no válido: {tipo}")

class NFTFactory:
    @staticmethod
    def create_token(tipo, owner, poll_id, opcion):
        token_id = str(uuid.uuid4())
        issued_at = datetime.utcnow()
        if tipo == "estandar":
            return StandardToken(token_id, owner, poll_id, opcion, issued_at)
        elif tipo == "limitado":
            return LimitedEditionToken(token_id, owner, poll_id, opcion, issued_at)
        else:
            raise ValueError(f"Tipo de token no válido: {tipo}")
