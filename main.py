import argparse
from src.config import DEFAULT_ZIP_PATH, DEFAULT_TARGET_PATH
from src.uploader import upload_zip_to_gcs

def main():
    parser = argparse.ArgumentParser(description="Subir imágenes de un ZIP a GCS sin descomprimir.")
    # Argumentos de línea de comandos.
    # Puedes configurar estos valores en un archivo .env o pasarlos directamente.
    parser.add_argument('--zip', type=str, default=DEFAULT_ZIP_PATH, help="Ruta local al archivo .zip") # Ruta del ZIP a descargar.
    parser.add_argument('--target', type=str, default=DEFAULT_TARGET_PATH, help="Ruta destino en GCS (dentro del bucket)") # Ruta destino en GCS.

    args = parser.parse_args()

    upload_zip_to_gcs(zip_path=args.zip, target_path=args.target)

if __name__ == "__main__":
    main()
