import cv2
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

RTSP_URL = os.getenv("RTSP_URL")

# Membuat folder penyimpanan video
FOLDER_VIDEO = "dataset/video"
os.makedirs(FOLDER_VIDEO, exist_ok=True)

# Timestamp otomatis
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# Nama file video
NAMA_VIDEO = os.path.join(
    FOLDER_VIDEO,
    f"video_bioflok_{timestamp}.mp4"
)

print("Menghubungkan ke kamera...")
cap = cv2.VideoCapture(RTSP_URL)

if not cap.isOpened():
    print("Gagal membuka kamera!")
    exit()

frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

fps = int(cap.get(cv2.CAP_PROP_FPS))
if fps <= 0:
    fps = 20

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(
    NAMA_VIDEO,
    fourcc,
    fps,
    (frame_width, frame_height)
)

print(f"Video akan disimpan sebagai:")
print(NAMA_VIDEO)
print("\nTekan 'Q' untuk berhenti merekam.\n")

while True:

    ret, frame = cap.read()

    if not ret:
        print("Koneksi kamera terputus.")
        break

    out.write(frame)

    cv2.imshow("Rekam CCTV Tapo", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Perekaman dihentikan.")
        break

cap.release()
out.release()
cv2.destroyAllWindows()

print("\nVideo berhasil disimpan:")
print(NAMA_VIDEO)