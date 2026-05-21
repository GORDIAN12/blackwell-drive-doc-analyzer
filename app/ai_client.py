import logging

from anthropic import Anthropic
from pydantic import ValidationError

from app.config import settings
from app.models import DocumentAnalysis


logger = logging.getLogger(__name__)


SYSTEM_PROMPT = """
Eres un analista senior de documentos de negocio.

Tu tarea es analizar documentos como propuestas comerciales, minutas,
reportes de avance y documentos operativos.

Reglas obligatorias:
- No inventes información.
- Si un dato no aparece en el documento, usa null o una lista vacía.
- El resumen ejecutivo debe tener entre 5 y 8 bullets.
- Los próximos pasos deben ser concretos, accionables y útiles para un equipo de trabajo.
- En cliente_o_proyecto escribe únicamente el nombre del cliente, empresa o proyecto principal. No incluyas subtítulos, objetivos, slogans ni descripciones largas.
- La clasificación debe ser exactamente una de estas:
  propuesta_comercial, minuta_reunion, reporte_avance, documento_operativo, otro.
- Devuelve la información usando únicamente la herramienta indicada.
"""


class AIClient:
    def __init__(self) -> None:
        self.client = Anthropic(api_key=settings.anthropic_api_key)
        self.model = settings.claude_model

    def analyze_document(self, document_name: str, text: str) -> DocumentAnalysis:
        if not text.strip():
            raise ValueError(f"El documento {document_name} no contiene texto extraíble.")

        limited_text = self._limit_text(text)

        tool_schema = DocumentAnalysis.model_json_schema()

        response = self.client.messages.create(
            model=self.model,
            max_tokens=2500,
            temperature=0,
            system=SYSTEM_PROMPT,
            tools=[
                {
                    "name": "save_document_analysis",
                    "description": "Guarda el análisis estructurado del documento.",
                    "input_schema": tool_schema,
                }
            ],
            tool_choice={
                "type": "tool",
                "name": "save_document_analysis",
            },
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"Analiza el siguiente documento.\n\n"
                        f"Nombre del documento: {document_name}\n\n"
                        f"Contenido:\n{limited_text}"
                    ),
                }
            ],
        )

        for block in response.content:
            if block.type == "tool_use" and block.name == "save_document_analysis":
                try:
                    return DocumentAnalysis.model_validate(block.input)
                except ValidationError as error:
                    logger.exception(
                        "La respuesta de IA no cumple con el esquema esperado: %s",
                        error,
                    )
                    raise

        raise ValueError("La IA no devolvió una llamada válida a la herramienta.")
    
    def _limit_text(self, text: str, max_chars: int = 50000) -> str:
        """
        Limita el texto para evitar enviar documentos demasiado grandes.
        Para esta prueba técnica es suficiente.
        """
        if len(text) <= max_chars:
            return text

        logger.warning(
            "Documento truncado: %s caracteres originales, %s enviados.",
            len(text),
            max_chars,
        )

        return text[:max_chars]