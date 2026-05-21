import json
import logging
from pathlib import Path
from typing import Any

from app.ai_client import AIClient
from app.config import settings
from app.drive_client import DriveClient
from app.models import DocumentMetadata, DocumentOutput
from app.readers import extract_text_from_bytes, is_supported_file
from app.utils import sanitize_filename


logger = logging.getLogger(__name__)


class DocumentProcessor:
    def __init__(self) -> None:
        self.drive = DriveClient()
        self.ai = AIClient()
        self.output_dir = Path(settings.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def process_folder(self, folder_id: str) -> list[Path]:
        files = self.drive.list_files_in_folder(folder_id)

        if not files:
            logger.warning("No se encontraron archivos en la carpeta.")
            return []

        logger.info("Archivos encontrados: %s", len(files))

        generated_outputs: list[Path] = []

        for file in files:
            try:
                output_path = self.process_file(file)
                generated_outputs.append(output_path)
            except Exception as error:
                logger.exception(
                    "Error procesando %s: %s",
                    file.get("name", "archivo_desconocido"),
                    error,
                )
                continue

        return generated_outputs

    def process_file(self, file: dict[str, Any]) -> Path:
        file_id = file["id"]
        file_name = file["name"]
        mime_type = file.get("mimeType")

        logger.info("Procesando archivo: %s | %s", file_name, mime_type)

        if not is_supported_file(file_name, mime_type):
            raise ValueError(f"Formato no soportado: {file_name}")

        content = self.drive.download_file(file_id, mime_type)
        text = extract_text_from_bytes(file_name, content, mime_type)

        if not text.strip():
            raise ValueError(f"No se pudo extraer texto de {file_name}")

        analysis = self.ai.analyze_document(file_name, text)

        output = DocumentOutput(
            documento=DocumentMetadata(
                id=file_id,
                nombre=file_name,
                mime_type=mime_type,
            ),
            analisis=analysis,
        )

        output_path = self._save_output(output)

        logger.info("Output generado: %s", output_path)

        return output_path

    def _save_output(self, output: DocumentOutput) -> Path:
        file_stem = Path(output.documento.nombre).stem
        safe_name = sanitize_filename(file_stem)

        output_path = self.output_dir / f"{safe_name}_{output.documento.id[:8]}.json"

        data = output.model_dump(mode="json")

        output_path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        return output_path