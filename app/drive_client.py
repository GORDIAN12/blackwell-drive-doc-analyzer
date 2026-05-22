import io
from pathlib import Path
from typing import Any
from google.auth.transport.requests import Request as GoogleAuthRequest
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

from app.config import settings


SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

GOOGLE_DOC_MIME_TYPE = "application/vnd.google-apps.document"
GOOGLE_DOC_EXPORT_MIME_TYPE = "text/plain"


class DriveClient:
# Inicializamos el cliente de drive con sus credenciales.
# Se usa en processor.py.
    def __init__(self) -> None:
        self.credentials_file = settings.google_credentials_file
        self.token_file = settings.google_token_file
        self.service = self._build_service()

    def _build_service(self) -> Any:
        creds = None

        token_path = Path(self.token_file)
        credentials_path = Path(self.credentials_file)

        if token_path.exists():
            creds = Credentials.from_authorized_user_file(
                str(token_path),
                SCOPES,
            )
    # Verificamos si las credenciales son validas y si no, las actualizamos.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(GoogleAuthRequest())
            else:
                if not credentials_path.exists():
                    raise FileNotFoundError(
                        f"No se encontró {self.credentials_file}. "
                        "Descarga tus credenciales OAuth desde Google Cloud Console."
                    )

                flow = InstalledAppFlow.from_client_secrets_file(
                    str(credentials_path),
                    SCOPES,
                )
                creds = flow.run_local_server(port=0)

            token_path.write_text(creds.to_json(), encoding="utf-8")

        return build("drive", "v3", credentials=creds)

    # Listamos los archivos de la carpeta de drive.
    # Se usa en processor.py.

    def list_files_in_folder(self, folder_id: str) -> list[dict[str, Any]]:
        files: list[dict[str, Any]] = []
        page_token = None

        query = f"'{folder_id}' in parents and trashed = false"

        while True:
            response = (
                self.service.files()
                .list(
                    q=query,
                    spaces="drive",
                    fields=(
                        "nextPageToken, "
                        "files(id, name, mimeType, size, modifiedTime, webViewLink)"
                    ),
                    pageToken=page_token,
                    supportsAllDrives=True,
                    includeItemsFromAllDrives=True,
                )
                .execute()
            )

            files.extend(response.get("files", []))
            page_token = response.get("nextPageToken")

            if not page_token:
                break

        return files

    # Descargamos el archivo de drive.
    # Se usa en processor.py.
    def download_file(self, file_id: str, mime_type: str) -> bytes:
        # Si el archivo es un documento de Google Docs, exportamos el texto plano.
        if mime_type == GOOGLE_DOC_MIME_TYPE:
            request = self.service.files().export_media(
                fileId=file_id,
                mimeType=GOOGLE_DOC_EXPORT_MIME_TYPE,
            )
        else:
            request = self.service.files().get_media(fileId=file_id)

        buffer = io.BytesIO()
        downloader = MediaIoBaseDownload(buffer, request)

        done = False

        while not done:
            _, done = downloader.next_chunk()

        return buffer.getvalue()