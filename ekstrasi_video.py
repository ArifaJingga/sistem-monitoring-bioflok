import cv2
import os
import glob # Library untuk mencari file dengan ekstensi tertentu

# 1. MENCARI SEMUA FILE VIDEO DI FOLDER INI
daftar_video = glob.glob("*.mp4")

if len(daftar_video) == 0:
    print("Tidak ditemukan file .mp4 di folder ini.")
    exit()

print("=== DAFTAR VIDEO REKAMAN ===")
for indeks, nama_file in enumerate(daftar_video):
    print(f"[{indeks}] {nama_file}")

# 2. MEMINTA PENGGUNA MEMILIH VIDEO
try:
    pilihan = int(input("\nMasukkan nomor video yang ingin diekstrak: "))
    NAMA_VIDEO = daftar_video[pilihan]
except (ValueError, IndexError):
    print("Nomor tidak valid! Program dihentikan.")
    exit()

# 3. MEMBUAT FOLDER HASIL YANG SPESIFIK
# Jika video bernama "rekaman_pagi.mp4", foldernya bernama "Dataset_Gambar/rekaman_pagi"
nama_folder_spesifik = NAMA_VIDEO.replace(".mp4", "")
FOLDER_HASIL = os.path.join("Dataset_Gambar", nama_folder_spesifik)
os.makedirs(FOLDER_HASIL, exist_ok=True)

print(f"\nMemproses: {NAMA_VIDEO}")
cap = cv2.VideoCapture(NAMA_VIDEO)

if not cap.isOpened():
    print(f"Gagal membuka video {NAMA_VIDEO}!")
    exit()

fps = int(cap.get(cv2.CAP_PROP_FPS))
if fps == 0: fps = 30 # Fallback jika metadata rusak
print(f"Mengekstrak otomatis 1 frame setiap detik (setiap {fps} frame)...")

frame_count = 0
saved_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Simpan 1 gambar setiap tepat 1 detik berlalu
    if frame_count % fps == 0:
        filename = f"frame_{saved_count:04d}.jpg"
        filepath = os.path.join(FOLDER_HASIL, filename)
        cv2.imwrite(filepath, frame)
        saved_count += 1

    frame_count += 1

cap.release()
print(f"Selesai! {saved_count} frame berhasil diekstrak ke dalam folder: {FOLDER_HASIL}")