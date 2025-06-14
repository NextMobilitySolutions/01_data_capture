import cv2
import os
import zipfile
import io

# Carpeta con los vídeos
input_folder = 'videos'
# Carpeta donde se guardarán los .zip finales
output_folder = 'data'
os.makedirs(output_folder, exist_ok=True)

# Recorrer vídeos
for video_file in os.listdir(input_folder):
    if not video_file.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
        continue

    video_path = os.path.join(input_folder, video_file)
    video_name = os.path.splitext(video_file)[0]
    zip_path = os.path.join(output_folder, f"{video_name}.zip")

    print(f"Procesando {video_name}...")

    cap = cv2.VideoCapture(video_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_number = 0
    saved_count = 0

    with zipfile.ZipFile(zip_path, 'w', compression=zipfile.ZIP_DEFLATED) as zipf:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            if frame_number % fps == 0:
                # Codificar imagen en memoria (JPG)
                success, buffer = cv2.imencode('.jpg', frame)
                if success:
                    img_bytes = buffer.tobytes()
                    img_name = f"{video_name}/frame_{saved_count:05d}.jpg"
                    zipf.writestr(img_name, img_bytes)
                    saved_count += 1

            frame_number += 1

    cap.release()
    print(f"{saved_count} frames guardados en {zip_path}")

print("Extracción y compresión finalizadas sin uso de disco temporal.")
