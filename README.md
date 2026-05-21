# Blackwell Doc AI

Este proyecto automatiza la descarga de documentos desde Google Drive, la extracción de su texto y el procesamiento del contenido utilizando la API de Anthropic.

---

## 1. Estructura del Proyecto

```bash
prueba_tecnica/
│
├── app/
│   ├── main.py              # Punto de entrada de la CLI
│   ├── config.py            # Carga de variables de entorno (.env)
│   ├── models.py            # Esquemas Pydantic para estructurar el output
│   ├── drive_client.py      # Autenticación, listado y descarga de Drive
│   ├── readers.py           # Extracción de texto (txt, md, pdf, docx)
│   ├── ai_client.py         # Integración y llamadas a Anthropic
│   ├── processor.py         # Orquestador del flujo por documento
│   └── utils.py             # Helpers: formateo de nombres, logs y sanitización
│
├── outputs/                 # Carpeta local para resultados generados
├── credentials.json         # Credenciales OAuth de Google Cloud (Ignorado)
├── token.json               # Token de acceso de usuario (Ignorado)
├── .env.example             # Plantilla de variables de entorno
├── requirements.txt         # Dependencias del proyecto
└── README.md                # Documentación
```
## 2. Configuracion de virtual enviroment
```
# Crear el entorno virtual en la raíz del proyecto
python3 -m venv .venv

# Activar el entorno virtual
source .venv/bin/activate
```

## 3. Instalacion de dependencias
```
pip install -r requirements.txt
```
## 4. Configuración de APIs y Variables de Entorno

Para que el proyecto funcione correctamente, es necesario configurar las llaves de acceso y las rutas del sistema en un archivo `.env`.

### Crear el archivo .env
Copia la plantilla de ejemplo `.env.example` para crear tu archivo de configuración local ejecutando en tu terminal:

```bash
cp .env.example .env
```
Modificamos  nuestras credenciales con los que se pide en nuestro archivo .env, agregando nuestra api de nuestro agente de anthropic y el modelo a usar del agente.

```
ANTHROPIC_API_KEY=tu_api_key_real      # Key privada de la consola de anthropic (https://console.anthropic.com/) 
CLAUDE_MODEL=claude-3-5-sonnet-latest  # Modelo de Claude a utilizar por el agente 

GOOGLE_CREDENTIALS_FILE=credentials.json   # Archivo JSON de credenciales descargado de Google Cloud
GOOGLE_TOKEN_FILE=token.json               # Archivo donde se guardará el token de sesión generado automáticamente

OUTPUT_DIR=outputs                      #Carpeta local donde se exportarán los resultados del procesamiento
LOG_FILE=logs/app.log                   #Ruta del archivo para el almacenamiento de logs y errores
```
### ¿Cómo obtener el archivo credentials.json?

Puedes generar y descargar este archivo desde la consola de Google Cloud. Si necesitas una guía visual paso a paso de cómo realizar la configuración, la pantalla de consentimiento OAuth y la descarga del cliente, revisa el material de apoyo que se encuentra en la siguiente carpeta de este repositorio:

 `app/google_cloud_configuration/STEPS_API.md`

Una vez descargado el archivo, muévelo a la raíz del proyecto y asegúrate de renombrarlo exactamente como `credentials.json`.


## 5. Ejecución del Proyecto

Para procesar los documentos de una carpeta de Google Drive, necesitas obtener su identificador único (**Folder ID**) y pasarlo como argumento al script.

### Obtener el ID de la carpeta de Google Drive
Abre la carpeta en tu navegador y copia únicamente la cadena de caracteres que aparece al final de la URL, después de `/folders/`:

```text
[https://drive.google.com/drive/folders/101FvmqAxuxxxyyyyxxyyy]
```
### Ejecutar procesamiento de archivos.
 
```
python -m app.main --folder-id SUSTITUYE_AQUI_LA_DIRECCION_CARPETA
```

Generando los archivos 