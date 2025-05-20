from dataclasses import dataclass
from datetime import datetime

@dataclass
class Poll:
    id: str
    pregunta: str
    opciones: dict  # {opcion: votos}
    estado: str  # activa / cerrada
    timestamp_inicio: datetime
    timestamp_fin: datetime
    tipo: str  # simple / multiple / ponderada
