# app/domain/decision_context.py
from typing import Optional

class DecisionContext:

    def __init__(
        self,
        solicitud,
        ocr_nomina,
        ocr_identidad,
        datacredito,
    ):
        # inputs técnicos (se mantienen)
        self.solicitud = solicitud
        self.ocr_nomina = ocr_nomina
        self.ocr_identidad = ocr_identidad
        self.datacredito = datacredito

        # 👇 variables de negocio (esto faltaba)
        self.ingreso_neto_mensual: Optional[float] = None
        self.porcentaje_descuento_nomina: Optional[float] = None
        self.edad_actual: Optional[int] = None
        self.edad_al_vencimiento: Optional[int] = None
        self.mora_activa: Optional[bool] = None
        self.tuvo_castigos: Optional[bool] = None
        self.score_datacredtio: Optional[bool] = None
        self.validacion_ocr_exitosa: bool = False
        self.pagador: Optional[str] = None
