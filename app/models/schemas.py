from pydantic import BaseModel, Field
from typing import Optional, List, Literal
from datetime import datetime, date
from enum import Enum
# app/models/schemas.py
from app.models.enums import TipoCliente

class SolicitudCreditoRequest(BaseModel):
    # Identificación
    numero_documento: str = Field(..., example="1234567890")

    # Perfil del solicitante
    tipo_cliente: TipoCliente = Field(
        ...,
        description="Tipo de cliente según su fuente de ingreso principal"
    )
    pagador: str = Field(..., example="FONDO_NACIONAL_MAGISTERIO")

    # Datos financieros declarados
    ingreso_bruto_mensual: float = Field(..., example=6000000)
    #ingreso declarado por el cliente que será validado contra el OCR
   
    # Datos laborales (declarados)
    antiguedad_laboral_anios: int = Field(
        ...,
        ge=0,
        example=7,
        description="Antigüedad laboral aproximada en años"
    )

    antiguedad_laboral_meses_adicionales: Optional[int] = Field(
        None,
        ge=0,
        le=11,
        example=3,
        description="Meses adicionales sobre los años completos (opcional)"
    )

    # Crédito solicitado
    monto_solicitado: float = Field(..., example=30000000)
    plazo_meses_solicitado: int = Field(..., example=72)

    # Archivos
    desprendible_nomina_base64: Optional[str] = Field(
        None,
        description="Archivo del desprendible de pago en base64"
    )

    #cedula
    archivo_identidad: Optional[str]=Field(None,
        description="foto de la cedula"
        )

# hay que eliminarlo despues
class DatosOCRNomina(BaseModel):
    ingreso_bruto: float
    descuentos_ley: float
    otros_descuentos: float
    ingreso_neto: float

    pagador_detectado: str
    tipo_contrato_detectado: Optional[str]
# hay que eliminarlo despues
class DatosOCRIdentidad(BaseModel):
    numero_documento_detectado: str
    fecha_nacimiento: date
    tipo_documento: Literal["CC", "CE", "TI"]

    nombres: Optional[str]
    apellidos: Optional[str]    
# hay que eliminarlo despues
class DatosDatacredito(BaseModel):
    score_datacredito: int = Field(..., example=720)
    mora_historica_dias: int = Field(..., example=0)
    numero_obligaciones_mora: int = Field(..., example=0)
    castigos_historicos: bool = Field(..., example=False)
    normalizacion_reciente: bool = Field(..., example=False)

class VariablesModelo(BaseModel):
    porcentaje_descuento_nomina: float
    ingreso_neto_mensual: float
    score_datacredito: int
    mora_historica_dias: int
    antiguedad_laboral_anios: int
    edad: int
    plazo_meses: int

class ResultadoScoreBase(BaseModel):
    score_base: int = Field(..., ge=0, le=1000)

class AjusteScore(BaseModel):
    nombre_ajuste: str
    impacto_score: int
    motivo: str

class AjustesScoreInput(BaseModel):
    """
    Variables cualitativas y de comportamiento
    que generan ajustes positivos o negativos al score base
    """

    # Perfil del cliente
    pensionado_vitalicio: bool = Field(
        ...,
        description="Indica si el cliente es pensionado vitalicio"
    )

    # Pagador
    pagador_puntual: Optional[bool] = Field(
    None,
    description="Indica si el pagador tiene historial puntual"
    )

    pagador_con_sla_contractual: bool = Field(
        ...,
        description="Pagador cuenta con SLA contractual de pago"
    )

    # Comportamiento histórico
    historial_reprocesos: int = Field(
        ...,
        ge=0,
        description="Número de reprocesos históricos del cliente"
    )

    # Endeudamiento por libranza
    numero_libranzas_activas: int = Field(
        ...,
        ge=0,
        description="Cantidad de libranzas activas registradas"
    )

    # Ingresos
    ingresos_adicionales_recurrentes: bool = Field(
        ...,
        description="Cliente cuenta con ingresos adicionales recurrentes"
    )

    # Eventos de riesgo recientes
    reestructuracion_meses: Optional[int] = Field(
        None,
        ge=0,
        description="Meses transcurridos desde la última reestructuración"
    )

    normalizacion_meses: Optional[int] = Field(
        None,
        ge=0,
        description="Meses transcurridos desde la normalización de mora"
    )

class ResultadoScoreFinal(BaseModel):
    score_ajustado: int = Field(..., ge=0, le=1000)
    banda_riesgo: Literal["A+", "A", "B", "C", "RECHAZO"]
    ajustes_aplicados: List[AjusteScore]

class DecisionCredito(BaseModel):
    aprobado: bool
    monto_aprobado: Optional[float]
    tasa_interes_mensual: Optional[float]
    plazo_meses: Optional[int]
    couta_mensual: Optional[float]

    motivo_rechazo: Optional[str]
    pd_estimado: Optional[float]

class EvaluacionCreditoResponse(BaseModel):
    variables_modelo: VariablesModelo
    score_base: ResultadoScoreBase
    score_final: ResultadoScoreFinal
    decision: DecisionCredito
    fecha_evaluacion: datetime = Field(default_factory=datetime.utcnow)







