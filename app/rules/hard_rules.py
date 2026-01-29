from dataclasses import dataclass
from typing import Optional, Dict, Any

from app.domain.decision_context import DecisionContext


# ================= RESULTADO =================

@dataclass
class HardRuleResult:
    aprobado: bool
    regla_violada: Optional[str] = None
    codigo_rechazo: Optional[str] = None
    motivo_rechazo: Optional[str] = None
    detalle: Optional[Dict[str, Any]] = None


# ================= VALIDATOR =================

class HardRulesValidator:

    LIMITE_ENDEUDAMIENTO_ACTUAL = 0.5
    INGRESO_NETO_MINIMO = 1_750_905
    EDAD_MINIMA = 20
    EDAD_MAXIMA_VENCIMIENTO = 75

    PAGADORES_AUTORIZADOS = {
        "SECRETARIA_EDUCACION_ANTIOQUIA",
        "SECRETARIA_EDUCACION_ATLANTICO",
        "SECRETARIA_EDUCACION_BOGOTA",
        "SECRETARIA_EDUCACION_BOLIVAR",
        "SECRETARIA_EDUCACION_BOYACA",
        "SECRETARIA_EDUCACION_CALDAS",
        "SECRETARIA_EDUCACION_CAQUETA",
        "SECRETARIA_EDUCACION_CASANARE",
        "SECRETARIA_EDUCACION_CAUCA",
        "SECRETARIA_EDUCACION_CESAR",
        "SECRETARIA_EDUCACION_CHOCO",
        "SECRETARIA_EDUCACION_CORDOBA",
        "SECRETARIA_EDUCACION_CUNDINAMARCA",
        "SECRETARIA_EDUCACION_GUAINIA",
        "SECRETARIA_EDUCACION_GUAVIARE",
        "SECRETARIA_EDUCACION_HUILA",
        "SECRETARIA_EDUCACION_LA_GUAJIRA",
        "SECRETARIA_EDUCACION_MAGDALENA",
        "SECRETARIA_EDUCACION_META",
        "SECRETARIA_EDUCACION_NARINO",
        "SECRETARIA_EDUCACION_NORTE_SANTANDER",
        "SECRETARIA_EDUCACION_PUTUMAYO",
        "SECRETARIA_EDUCACION_QUINDIO",
        "SECRETARIA_EDUCACION_RISARALDA",
        "SECRETARIA_EDUCACION_SAN_ANDRES",
        "SECRETARIA_EDUCACION_SANTANDER",
        "SECRETARIA_EDUCACION_SUCRE",
        "SECRETARIA_EDUCACION_TOLIMA",
        "SECRETARIA_EDUCACION_VALLE",
        "SECRETARIA_EDUCACION_VAUPES",
        "SECRETARIA_EDUCACION_VICHADA",
        "FONDO_NACIONAL_MAGISTERIO",
        "FIDUPREVISORA",
        "FOMAG",
    }

    # ================= ENTRY POINT =================

    def validar(self, context: DecisionContext) -> HardRuleResult:

        # ---------- VALIDACIÓN OCR ----------
        if not context.validacion_ocr_exitosa:
            return self._rechazar(
                "HR-01",
                "OCR_INVALIDO",
                "No fue posible validar correctamente los documentos"
            )

        # ---------- PAGADOR ----------
        resultado = self._validar_pagador(context.pagador)
        if not resultado.aprobado:
            return resultado

        # ---------- INGRESO ----------
        if context.ingreso_neto_mensual is None:
            return self._rechazar(
                "HR-03",
                "INGRESO_NO_DETECTADO",
                "No fue posible detectar el ingreso"
            )

        resultado = self._validar_ingreso_minimo(context.ingreso_neto_mensual)
        if not resultado.aprobado:
            return resultado

        # ---------- ENDEUDAMIENTO ----------
        if context.porcentaje_descuento_nomina is None:
            return self._rechazar(
                "HR-07",
                "DESCUENTOS_NO_DETECTADOS",
                "No fue posible calcular el endeudamiento"
            )

        resultado = self._validar_endeudamiento_actual(
            context.porcentaje_descuento_nomina
        )
        if not resultado.aprobado:
            return resultado

        # ---------- EDAD ----------
        if context.edad_actual is None:
            return self._rechazar(
                "HR-05",
                "EDAD_NO_DETECTADA",
                "No fue posible validar la edad"
            )

        if context.edad_al_vencimiento is None:
            return self._rechazar(
                "HR-05",
                "EDAD_VENCIMIENTO_NO_DEFINIDA",
                "No fue posible calcular la edad al vencimiento"
            )

        resultado = self._validar_edad_actual(context.edad_actual)
        if not resultado.aprobado:
            return resultado

        resultado = self._validar_edad_vencimiento(
            context.edad_al_vencimiento
        )
        if not resultado.aprobado:
            return resultado

        # ---------- DATA CRÉDITO ----------
        if context.mora_activa:
            return self._rechazar(
                "HR-06",
                "MORA_ACTIVA",
                "El solicitante tiene mora activa"
            )

        return HardRuleResult(aprobado=True)

    # ================= VALIDACIONES =================

    def _validar_pagador(self, pagador: Optional[str]) -> HardRuleResult:
        if not pagador:
            return self._rechazar(
                "HR-02",
                "PAGADOR_NO_DETECTADO",
                "No fue posible detectar el pagador"
            )

        pagador_norm = pagador.upper().replace(" ", "_")

        if pagador_norm not in self.PAGADORES_AUTORIZADOS:
            return self._rechazar(
                "HR-02",
                "PAGADOR_NO_AUTORIZADO",
                f"Pagador {pagador} no autorizado"
            )

        return HardRuleResult(aprobado=True)

    def _validar_ingreso_minimo(self, ingreso: float) -> HardRuleResult:
        if ingreso < self.INGRESO_NETO_MINIMO:
            return self._rechazar(
                "HR-04",
                "INGRESO_INSUFICIENTE",
                "Ingreso neto insuficiente"
            )
        return HardRuleResult(aprobado=True)

    def _validar_endeudamiento_actual(self, porcentaje: float) -> HardRuleResult:
        if porcentaje >= self.LIMITE_ENDEUDAMIENTO_ACTUAL:
            return self._rechazar(
                "HR-07",
                "ENDEUDAMIENTO_EXCEDIDO",
                "Endeudamiento actual excede el límite"
            )
        return HardRuleResult(aprobado=True)

    def _validar_edad_actual(self, edad: int) -> HardRuleResult:
        if edad < self.EDAD_MINIMA:
            return self._rechazar(
                "HR-05",
                "EDAD_MINIMA_NO_CUMPLIDA",
                "No cumple edad mínima"
            )
        return HardRuleResult(aprobado=True)

    def _validar_edad_vencimiento(self, edad_vencimiento: int) -> HardRuleResult:
        if edad_vencimiento > self.EDAD_MAXIMA_VENCIMIENTO:
            return self._rechazar(
                "HR-08",
                "EDAD_VENCIMIENTO_EXCEDIDA",
                "Edad al vencimiento excede el máximo permitido"
            )
        return HardRuleResult(aprobado=True)

    def _rechazar(self, regla, codigo, motivo) -> HardRuleResult:
        return HardRuleResult(
            aprobado=False,
            regla_violada=regla,
            codigo_rechazo=codigo,
            motivo_rechazo=motivo
        )
    