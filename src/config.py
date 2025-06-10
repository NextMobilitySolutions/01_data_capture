import os
from dotenv import load_dotenv

# Carga del archivo .env
load_dotenv()

# Variables base del entorno.
PROJECT_ID = os.getenv("PROJECT_ID")
BUCKET_NAME = os.getenv("BUCKET_NAME")

# Opcional por defecto: Ruta de destino en GCS y ruta del ZIP. Debe ser configurada en el .env si se desea cambiar.
DEFAULT_TARGET_PATH = os.getenv("DEFAULT_TARGET_PATH", "raw/public/bdd100k") # Ruta destino en GCS.
DEFAULT_ZIP_PATH = os.getenv("DEFAULT_ZIP_PATH", "data/bdd100k_images_10k.zip") # Ruta del ZIP a descargar.

# Validación mínima.
if not PROJECT_ID or not BUCKET_NAME:
    raise ValueError("Faltan variables obligatorias PROJECT_ID o BUCKET_NAME en el .env")
