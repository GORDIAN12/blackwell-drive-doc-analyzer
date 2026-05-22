import io
from pathlib import Path

from docx import Document
from pypdf import PdfReader


SUPPORTED_EXTENSIONS = {
    ".txt",
    ".md",
    ".pdf",
    ".docx",
}


GOOGLE_DOC_MIME_TYPE = "application/vnd.google-apps.document"

    
# Verifica si el archivo puede procesarse.
def is_supported_file(file_name: str, mime_type: str | None = None) -> bool:
    suffix = Path(file_name).suffix.lower()

    if suffix in SUPPORTED_EXTENSIONS:
        return True

    if mime_type == GOOGLE_DOC_MIME_TYPE:
        return True

    return False


def extract_text_from_bytes(
    file_name: str,
    content: bytes,
    mime_type: str | None = None,
) -> str:
    suffix = Path(file_name).suffix.lower()

    if suffix in {".txt", ".md"}:
        return _extract_plain_text(content)

    if suffix == ".pdf":
        return _extract_pdf_text(content)

    if suffix == ".docx":
        return _extract_docx_text(content)

    if mime_type == GOOGLE_DOC_MIME_TYPE:
        return _extract_plain_text(content)

    raise ValueError(f"Formato no soportado: {file_name}")


# Extrae el texto de un archivo de texto plano.
def _extract_plain_text(content: bytes) -> str:
    try:
        return content.decode("utf-8")
    except UnicodeDecodeError:
        return content.decode("latin-1")


#Extraemos el texto de un archivo PDF retornando el texto unido de todas las paginas."""
def _extract_pdf_text(content: bytes) -> str:
    reader = PdfReader(io.BytesIO(content))

    pages_text: list[str] = []

    for page in reader.pages:
        text = page.extract_text() or ""
        pages_text.append(text)

    return "\n\n".join(pages_text).strip()

#Extraemos el texto de un archivo DOCX retornando el texto unido.
def _extract_docx_text(content: bytes) -> str:
    document = Document(io.BytesIO(content))

    paragraphs = [
        paragraph.text.strip()
        for paragraph in document.paragraphs
        if paragraph.text.strip()
    ]

    return "\n".join(paragraphs).strip()