import cv2
import os
import glob
import subprocess  # Library bawaan Python (TIDAK perlu instal)

# 1. MENCARI SEMUA FILE VIDEO DI FOLDER
daftar_video = glob.glob("**/*.mp4", recursive=True)

if len(daftar_video) == 0:
    print("Tidak ditemukan file .mp4 di folder proyek ini.")
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

# 3. PERSIAPAN FOLDER LOKAL DI LAPTOP
nama_folder_spesifik = NAMA_VIDEO.replace(".mp4", "")
FOLDER_HASIL = os.path.join("Dataset_Gambar", nama_folder_spesifik)
os.makedirs(FOLDER_HASIL, exist_ok=True)

cap = cv2.VideoCapture(NAMA_VIDEO)
fps = int(cap.get(cv2.CAP_PROP_FPS))
if fps == 0: fps = 30

frame_count = 0
saved_count = 0

print(f"\n[1/2] Memproses ekstraksi {NAMA_VIDEO} secara lokal...")

# 4. PROSES EKSTRAKSI GAMBAR (DI LAPTOP)
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Ekstrak 1 gambar setiap 1 detik
    if frame_count % fps == 0:
        filename = f"frame_{saved_count:04d}.jpg"
        filepath = os.path.join(FOLDER_HASIL, filename)
        
        # Simpan di laptop
        cv2.imwrite(filepath, frame)
        saved_count += 1

    frame_count += 1

cap.release()
print(f"✔ Selesai! {saved_count} gambar tersimpan di folder lokal: {FOLDER_HASIL}")

# 5. OTOMATISASI TRANSFER KE RASPBERRY PI VIA SCP
print(f"\n[2/2] Menghubungkan ke Raspberry Pi via SCP untuk mengirim folder...")

perintah_scp = f'scp -O -r "{FOLDER_HASIL}" livinglab@192.168.88.88:/home/livinglab/workspace/arifa'

# Kita simpan hasil eksekusinya ke dalam variabel "hasil_scp"
hasil_scp = subprocess.run(perintah_scp, shell=True)

print(f"\n=== STATUS PENGIRIMAN ===")
# Jika kode kembaliannya 0, berarti SCP sukses tanpa error
if hasil_scp.returncode == 0:
    print(f"✔ SUKSES: Folder {nama_folder_spesifik} berhasil terkirim ke server Raspberry Pi!")
else:
    print(f"✖ GAGAL: Data tersimpan di laptop, tapi gagal dikirim ke server. Pastikan koneksi Wi-Fi Lab aktif!")