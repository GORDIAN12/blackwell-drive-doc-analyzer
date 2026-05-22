import hashlib
import logging
import re
import unicodedata
from pathlib import Path

from app.config import settings

"""Configura los logs del sistema y se usa al iniciar el programa en main.py"""

def setup_logging() -> None:
    log_path = Path(settings.log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[
            logging.FileHandler(log_path, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )

""" Limpia un texto para usarlo como parte de un nombre de archivo.
    Se usa al guardar los outputs JSON en processor.py ya que regresa el texto normalizado."""
def slugify(
    value: str | None,
    fallback: str = "sin_dato",
    max_length: int = 60,
) -> str:
    if not value:
        return fallback

    value = remove_accents(value)
    value = value.lower().strip()
    value = re.sub(r"[^\w\s-]", "", value, flags=re.UNICODE)
    value = re.sub(r"\s+", "_", value)
    value = re.sub(r"_+", "_", value)
    value = value.strip("_")

    if not value:
        return fallback

    if len(value) > max_length:
        value = value[:max_length].rstrip("_")

    return value

"""Elimina los acentos de un texto se usa dentro de slugify"""
def remove_accents(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    return "".join(char for char in normalized if not unicodedata.combining(char))


"""Genera un hash corto a partir de un texto evitando nombres de archivo duplicados."""

def short_hash(value: str, length: int = 8) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:length]