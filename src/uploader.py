import io
import zipfile
from google.cloud import storage
from pathlib import Path
from src.config import PROJECT_ID, BUCKET_NAME

def upload_zip_to_gcs(zip_path, target_path):
    """
    Sube un archivo ZIP a Google Cloud Storage, extrayendo solo las imágenes sin descomprimir el ZIP localmente.
    Params:
        zip_path (str): Ruta local del archivo ZIP a subir.
        target_path (str): Ruta en el bucket de GCS donde se subirán las imágenes.
    Returns:
        None
    """
    # Validación de entrada.
    print(f"Leyendo ZIP: {zip_path}")

    # Inicializa el cliente de GCS.
    client = storage.Client(project=PROJECT_ID)
    bucket = client.bucket(BUCKET_NAME)

    # Verifica que el archivo ZIP exista.
    with open(zip_path, "rb") as f:
        zip_bytes = io.BytesIO(f.read())

    print("Abriendo ZIP en memoria...") # Evita descomprimir localmente.
    with zipfile.ZipFile(zip_bytes, 'r') as zip_ref:
        image_files = [f for f in zip_ref.namelist() if f.lower().endswith((".jpg", ".jpeg", ".png"))]

        print(f"{len(image_files)} imágenes encontradas en el ZIP. Subiendo a: gs://{BUCKET_NAME}/{target_path}/")
        for img_name in image_files:
            with zip_ref.open(img_name) as img_file:
                # Mantener toda la ruta relativa tal como está en el ZIP
                relative_path = Path(img_name)
                blob_path = f"{target_path}/{relative_path}".replace("\\", "/")

                blob = bucket.blob(blob_path)
                blob.upload_from_file(img_file, content_type="image/jpeg")
                print(f"Subido: {blob_path}")

    print("Subida completa sin guardar archivos localmente.")
