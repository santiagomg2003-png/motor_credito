from enum import Enum

class TipoCliente(str, Enum):
    PENSIONADO = "PENSIONADO"
    DOCENTE = "DOCENTE"