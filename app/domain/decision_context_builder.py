# app/domain/decision_context_builder.py

from datetime import date
from app.domain.decision_context import DecisionContext

class DecisionContextBuilder:

    def build(self, solicitud, ocr_nomina, ocr_identidad, datacredito):

        context = DecisionContext(
            solicitud=solicitud,
            ocr_nomina=ocr_nomina,
            ocr_identidad=ocr_identidad,
            datacredito=datacredito
        )

        # ---------- INGRESO ----------
        if ocr_nomina:
            context.ingreso_neto_mensual = ocr_nomina.ingreso_neto
            context.pagador = ocr_nomina.pagador_detectado

            total_descuentos = (
            ocr_nomina.descuentos_ley + ocr_nomina.otros_descuentos
            )

        if ocr_nomina.ingreso_bruto and ocr_nomina.ingreso_bruto > 0:
            context.porcentaje_descuento_nomina = (
            total_descuentos / ocr_nomina.ingreso_bruto
            )
        else:
            context.porcentaje_descuento_nomina = None

        # ---------- EDAD ----------
        if ocr_identidad and ocr_identidad.edad_calculada is not None:
            context.edad_actual = ocr_identidad.edad_calculada

        if (
        context.edad_actual is not None
        and solicitud.plazo_meses_solicitado is not None
        ):
            plazo_anios = solicitud.plazo_meses_solicitado / 12
        context.edad_al_vencimiento = int(
        context.edad_actual + plazo_anios
        )

        # ---------- DATA CRÉDITO ----------
        if datacredito:
            context.mora_activa = datacredito.numero_obligaciones_mora > 0
            context.tuvo_castigos = datacredito.castigos_historicos
            context.score_datacredito = datacredito.score_datacredito

        # ---------- VALIDACIÓN ----------
        context.validacion_ocr_exitosa = (
            ocr_nomina is not None and ocr_identidad is not None
        )

        return context
    