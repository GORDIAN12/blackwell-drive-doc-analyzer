import argparse
import logging

from app.processor import DocumentProcessor
from app.utils import setup_logging


logger = logging.getLogger(__name__)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Procesador de documentos desde Google Drive usando IA."
    )

    parser.add_argument(
        "--folder-id",
        required=True,
        help="ID de la carpeta de Google Drive.",
    )

    args = parser.parse_args()

    setup_logging()

    logger.info("Iniciando procesamiento de documentos")
    logger.info("Folder ID: %s", args.folder_id)

    processor = DocumentProcessor()
    outputs = processor.process_folder(args.folder_id)

    logger.info("Procesamiento terminado. Outputs generados: %s", len(outputs))

    if outputs:
        print("\nArchivos generados:")
        for output in outputs:
            print(f"- {output}")
    else:
        print("\nNo se generaron archivos de salida.")


if __name__ == "__main__":
    main()