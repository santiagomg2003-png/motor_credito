from .base import OCRIdentidadService
from .types import OCRIdentidadResult
import random
from datetime import date

class MockOCRIdentidadService(OCRIdentidadService):

    def procesar_documento(self, imagen_base64: str):

        escenario = random.choice(["ok", "menor", "ilegible", "fallido"])

        if escenario == "fallido":
            return None

        if escenario == "ilegible":
            return OCRIdentidadResult(
                numero_documento="",
                tipo_documento="CC",
                nombres="",
                apellidos="",
                fecha_nacimiento=None,
                edad_calculada=None,
                sexo=None,
                nacionalidad=None,
                documento_valido=False
            )

        if escenario == "menor":
            return OCRIdentidadResult(
                numero_documento="1234567890",
                tipo_documento="CC",
                nombres="Juan",
                apellidos="Pérez",
                fecha_nacimiento=date(2010, 5, 20),
                edad_calculada=14,
                sexo="M",
                nacionalidad="CO",
                documento_valido=True
            )

        # escenario OK
        return OCRIdentidadResult(
            numero_documento="1234567890",
            tipo_documento="CC",
            nombres="Juan",
            apellidos="Pérez",
            fecha_nacimiento=date(1995, 3, 15),
            edad_calculada=29,
            sexo="M",
            nacionalidad="CO",
            documento_valido=True
        )
        