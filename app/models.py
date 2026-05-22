from typing import Literal
from pydantic import BaseModel, Field

# Establecemos las categorias de documentos posibles.
DocumentCategory = Literal[
    "propuesta_comercial",
    "minuta_reunion",
    "reporte_avance",
    "documento_operativo",
    "otro",
]


class DocumentMetadata(BaseModel):
    id: str
    nombre: str
    mime_type: str | None = None

# En este modelo se establecen los campos que debe extrar el agente, retornando la estructura establecida 
class StructuredExtraction(BaseModel):
    cliente_o_proyecto: str | None = None
    objetivo_principal: str | None = None
    entregables: list[str] = Field(default_factory=list)
    fechas_y_plazos: list[str] = Field(default_factory=list)
    responsables: list[str] = Field(default_factory=list)
    riesgos: list[str] = Field(default_factory=list)

# Modelo para el analisis de los documentos procesados establecinedo la estrucutra de datos para retornar.
class DocumentAnalysis(BaseModel):
    resumen_ejecutivo: list[str] = Field(
        min_length=5,
        max_length=8,
        description="Resumen ejecutivo en 5 a 8 bullets.",
    )
    extraccion_estructurada: StructuredExtraction
    clasificacion: DocumentCategory
    proximos_pasos: list[str] = Field(
        min_length=3,
        max_length=5,
        description="Próximos pasos concretos y accionables.",
    )

# Modelo para la salida de los documentos procesados usando de referencia a los modelos anteriores.
class DocumentOutput(BaseModel):
    documento: DocumentMetadata
    analisis: DocumentAnalysis