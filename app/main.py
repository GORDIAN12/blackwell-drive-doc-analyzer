import argparse
import logging

from app.drive_client import DriveClient
from app.readers import extract_text_from_bytes, is_supported_file
from app.utils import setup_logging


logger = logging.getLogger(__name__)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Procesador de documentos desde Google Drive."
    )

    parser.add_argument(
        "--folder-id",
        required=True,
        help="ID de la carpeta de Google Drive.",
    )

    args = parser.parse_args()

    setup_logging()

    logger.info("Iniciando conexión con Google Drive")

    drive = DriveClient()

    logger.info("Listando archivos de la carpeta: %s", args.folder_id)

    files = drive.list_files_in_folder(args.folder_id)

    if not files:
        logger.warning("No se encontraron archivos en la carpeta.")
        return

    logger.info("Archivos encontrados: %s", len(files))

    for file in files:
        file_id = file["id"]
        file_name = file["name"]
        mime_type = file.get("mimeType")

        logger.info("Archivo encontrado: %s | %s", file_name, mime_type)

        if not is_supported_file(file_name, mime_type):
            logger.warning("Archivo omitido por formato no soportado: %s", file_name)
            continue

        try:
            content = drive.download_file(file_id, mime_type)
            text = extract_text_from_bytes(file_name, content, mime_type)

            preview = text[:500].replace("\n", " ")

            logger.info("Texto extraído correctamente de: %s", file_name)
            print("\n" + "=" * 80)
            print(f"DOCUMENTO: {file_name}")
            print("-" * 80)
            print(preview)
            print("=" * 80 + "\n")

        except Exception as error:
            logger.exception("Error procesando %s: %s", file_name, error)
            continue


if __name__ == "__main__":
    main()