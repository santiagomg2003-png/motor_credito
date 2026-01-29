# app/api/evaluate.py

from fastapi import APIRouter
from datetime import date

from app.models.schemas import (
    SolicitudCreditoRequest,
    EvaluacionCreditoResponse,
    DatosOCRNomina,
    DatosDatacredito,
    DatosOCRIdentidad
)

from app.domain.decision_context_builder import DecisionContextBuilder
from app.rules.hard_rules import HardRulesValidator
# from app.domain.services.scoring_engine import ScoringEngine
# from app.domain.services.decision_engine import DecisionEngine

router = APIRouter()


@router.post(
    "/evaluate",
    response_model=EvaluacionCreditoResponse,
    summary="Evaluación de crédito"
)
def evaluar_credito(solicitud: SolicitudCreditoRequest):

    # -------------------------------------------------
    # 1️⃣ Inputs externos (MOCKS)
    # -------------------------------------------------

    ocr_nomina = DatosOCRNomina(
        ingreso_bruto=6_000_000,
        descuentos_ley=900_000,
        otros_descuentos=200_000,
        ingreso_neto=4_900_000,
        pagador_detectado=solicitud.pagador,
        tipo_contrato_detectado="PENSIONADO"
    )

    datacredito = DatosDatacredito(
        score_datacredito=720,
        mora_historica_dias=0,
        numero_obligaciones_mora=0,
        castigos_historicos=False,
        normalizacion_reciente=False
    )

    ocr_identidad = DatosOCRIdentidad(
        numero_documento=solicitud.numero_documento,
        tipo_documento=solicitud.tipo_documento,
        nombres="MOCK",
        apellidos="MOCK",
        fecha_nacimiento=date(1966, 5, 10),
        edad_calculada=58,
        sexo=None,
        nacionalidad=None,
        documento_valido=True
    )

    # -------------------------------------------------
    # 2️⃣ Construcción del Decision Context
    # -------------------------------------------------

    context = DecisionContextBuilder().build(
        solicitud=solicitud,
        ocr_nomina=ocr_nomina,
        ocr_identidad=ocr_identidad,
        datacredito=datacredito
    )

    # -------------------------------------------------
    # 3️⃣ Hard Rules
    # -------------------------------------------------

    hard_rules_engine = HardRulesValidator()
    resultado_hard_rules = hard_rules_engine.evaluar(context)

    if not resultado_hard_rules.aprobado:
        return EvaluacionCreditoResponse(
            decision=resultado_hard_rules
        )

    # -------------------------------------------------
    # 4️⃣ Scoring
    # -------------------------------------------------

    # scoring_engine = ScoringEngine()
   # score_final = scoring_engine.calcular(context)

    # -------------------------------------------------
    # 5️⃣ Decisión final
    # -------------------------------------------------

    # decision_engine = DecisionEngine()
   # decision = decision_engine.decidir(
        context=context,
        score_final=score_final
   # )

    # -------------------------------------------------
    # 6️⃣ Respuesta
    # -------------------------------------------------

   # return EvaluacionCreditoResponse(
        variables_modelo=context.to_variables_modelo(),
        score_base=score_final.score_base,
        score_final=score_final,
        decision=decision
   # )