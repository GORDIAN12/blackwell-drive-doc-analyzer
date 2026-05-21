from typing import Literal
from pydantic import BaseModel, Field


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


class StructuredExtraction(BaseModel):
    cliente_o_proyecto: str | None = None
    objetivo_principal: str | None = None
    entregables: list[str] = Field(default_factory=list)
    fechas_y_plazos: list[str] = Field(default_factory=list)
    responsables: list[str] = Field(default_factory=list)
    riesgos: list[str] = Field(default_factory=list)


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


class DocumentOutput(BaseModel):
    documento: DocumentMetadata
    analisis: DocumentAnalysis