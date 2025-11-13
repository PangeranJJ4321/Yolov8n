# 📷 Panduan Kalibrasi Kamera untuk Pothole Detection

## 🎯 Tujuan
Mendapatkan parameter intrinsik kamera (focal length, principal point, distortion) untuk konversi pixel ke metrik absolut dalam estimasi ukuran lubang.

## 📋 Persiapan

### 1. Cetak Checkerboard Pattern

#### Opsi Standar (9×6)
- **Ukuran kotak:** 25mm × 25mm (sesuai proposal)
- **Jumlah kotak:** 9×6 internal corners (10×7 total squares)
- **Total ukuran:** 250mm × 175mm

#### Opsi untuk Kertas A4 (Disarankan)
- **Ukuran kotak:** 25mm × 25mm
- **Jumlah kotak:** 7×10 internal corners (8×11 total squares)
- **Total ukuran:** 200mm × 275mm (muat di A4 210mm × 297mm dengan margin)
- **Keuntungan:** Lebih mudah dicetak di kertas A4 standar

#### Catatan Penting
- **Pattern size tidak harus 9×6** - bisa disesuaikan dengan kebutuhan
- **Yang penting:** Ukuran kotak harus diketahui dengan pasti (25mm) untuk kalibrasi metrik
- **Minimal pattern:** 6×4 internal corners untuk kalibrasi yang baik
- **Kualitas:** Cetak dengan printer berkualitas tinggi, pastikan pattern datar
- **Alternatif:** Download dari [OpenCV checkerboard generator](https://docs.opencv.org/4.x/da/df5/tutorial_py_calibration.html)

### 2. Setup Kamera
- **Mounting height:** Ukur tinggi kamera dari permukaan jalan (misal: 1.5m)
- **Pitch angle:** Catat sudut kemiringan kamera (jika ada)
- **Resolusi:** Gunakan resolusi yang akan dipakai untuk deteksi (misal: 1280×720)

## 📸 Pengambilan Gambar Kalibrasi

### Jumlah dan Variasi
- **Minimal:** 15-20 gambar
- **Ideal:** 25-30 gambar untuk akurasi tinggi

### Posisi dan Sudut
1. **Center:** Gambar dengan checkerboard di tengah frame
2. **Kiri/Kanan:** Checkerboard di sisi kiri dan kanan
3. **Atas/Bawah:** Checkerboard di bagian atas dan bawah
4. **Diagonal:** Posisi diagonal (kiri atas, kanan bawah, dll.)
5. **Jarak bervariasi:** Dekat (1-2m), sedang (3-5m), jauh (5-8m)

### Tips Pengambilan
- Pastikan seluruh checkerboard terlihat jelas
- Hindari blur (gunakan tripod jika perlu)
- Variasi pencahayaan (siang, sore, malam)
- Checkerboard harus datar (tidak melengkung)

## 🚀 Cara Menjalankan Kalibrasi

### 1. Siapkan Folder Gambar
```
G:/Yolov8n/calibration_images/
├── calib_001.jpg
├── calib_002.jpg
├── calib_003.jpg
└── ...
```

### 2. Jalankan Script Kalibrasi

#### Kalibrasi dengan Pattern Standar (9×6)
```powershell
# Kalibrasi baru dengan pattern default (9×6, 25mm)
G:\Yolov8n\yolov8\Scripts\python.exe G:\Yolov8n\camera_calibration.py --images G:/Yolov8n/calibration_images --output camera_params.yaml
```

#### Kalibrasi untuk Kertas A4 (7×10)
```powershell
# Kalibrasi dengan pattern A4 (7×10 internal corners, 25mm kotak)
G:\Yolov8n\yolov8\Scripts\python.exe G:\Yolov8n\camera_calibration.py --images G:/Yolov8n/calibration_images --output camera_params.yaml --pattern-size 7 10 --square-size 25
```

#### Pattern Kustom
```powershell
# Kalibrasi dengan pattern kustom (misal: 8×11, 20mm kotak)
G:\Yolov8n\yolov8\Scripts\python.exe G:\Yolov8n\camera_calibration.py --images G:/Yolov8n/calibration_images --output camera_params.yaml --pattern-size 8 11 --square-size 20
```

#### Test Parameter yang Sudah Ada
```powershell
# Test parameter yang sudah ada
G:\Yolov8n\yolov8\Scripts\python.exe G:\Yolov8n\camera_calibration.py --images G:/Yolov8n/calibration_images --load camera_params.yaml
```

#### Parameter Command Line
- `--images`: Path ke folder gambar kalibrasi (required)
- `--output`: File output untuk menyimpan parameter (default: `camera_params.yaml`)
- `--load`: Load parameter yang sudah ada untuk testing
- `--pattern-size WIDTH HEIGHT`: Pattern size internal corners (default: `9 6`)
- `--square-size SIZE`: Ukuran kotak dalam mm (default: `25.0`)

### 3. Output yang Dihasilkan
- `camera_params.yaml` - Parameter kamera (YAML)
- `camera_params.json` - Parameter kamera (JSON backup)
- `calibration_viz_*.jpg` - Visualisasi deteksi corners
- `undistort_test_*.jpg` - Test undistortion

## 📊 Interpretasi Hasil

### Parameter Penting
```yaml
camera_matrix: [[fx, 0, cx],
                [0, fy, cy],
                [0, 0, 1]]
distortion_coefficients: [k1, k2, p1, p2, k3]
```

- **fx, fy:** Focal length dalam pixel (untuk konversi metrik)
- **cx, cy:** Principal point (biasanya mendekati center image)
- **k1, k2, k3:** Radial distortion coefficients
- **p1, p2:** Tangential distortion coefficients

### Kriteria Kualitas
- **Reprojection error:** < 0.5 pixel (ideal), < 1.0 pixel (acceptable)
- **Successful images:** Minimal 10 dari total gambar
- **Focal length:** Harus positif dan reasonable

## ⚠️ Troubleshooting

### Masalah Umum
1. **"Tidak ditemukan corners"**
   - Pastikan checkerboard terlihat jelas
   - Coba gambar dengan pencahayaan lebih baik
   - Pastikan pattern tidak melengkung

2. **"Reprojection error tinggi"**
   - Tambah gambar kalibrasi
   - Pastikan variasi posisi dan sudut cukup
   - Cek kualitas gambar (tidak blur)

3. **"Minimal 10 gambar diperlukan"**
   - Ambil lebih banyak gambar dengan variasi posisi
   - Pastikan corners terdeteksi dengan baik

## 🔧 Penggunaan Parameter

### Load Parameter di Python
```python
import yaml
import numpy as np

# Load camera parameters
with open('camera_params.yaml', 'r') as f:
    params = yaml.safe_load(f)

K = np.array(params['camera_matrix'])
dist = np.array(params['distortion_coefficients'])
fx = K[0, 0]
fy = K[1, 1]
cx = K[0, 2]
cy = K[1, 2]

print(f"Focal length: fx={fx:.1f}, fy={fy:.1f}")
print(f"Principal point: cx={cx:.1f}, cy={cy:.1f}")
```

### Undistort Image
```python
import cv2

# Load image
img = cv2.imread('test_image.jpg')
h, w = img.shape[:2]

# Undistort
new_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(K, dist, (w, h), 1, (w, h))
undistorted = cv2.undistort(img, K, dist, None, new_camera_matrix)

# Save result
cv2.imwrite('undistorted.jpg', undistorted)
```

## 📝 Metadata Tambahan

Simpan juga informasi berikut untuk scale recovery:
```yaml
camera_metadata:
  mounting_height_m: 1.5  # Tinggi kamera dari jalan
  pitch_angle_deg: 0.0    # Sudut kemiringan kamera
  camera_model: "iPhone 12"
  resolution: [1280, 720]
  calibration_date: "2025-01-XX"
```

## ✅ Checklist Kalibrasi

- [ ] Checkerboard pattern dicetak (ukuran kotak diketahui dengan pasti, misal: 25mm×25mm)
- [ ] Pattern size sesuai dengan yang digunakan di script (cek dengan `--pattern-size`)
- [ ] 15-20 gambar kalibrasi dengan variasi posisi
- [ ] Script kalibrasi berjalan tanpa error
- [ ] Reprojection error < 0.5 pixel
- [ ] Parameter tersimpan ke YAML/JSON
- [ ] Test undistortion berhasil
- [ ] Metadata kamera dicatat (tinggi, sudut, dll.)

## 🎯 Langkah Selanjutnya

Setelah kalibrasi selesai:
1. **Integrasi DepthAnything V2** untuk estimasi kedalaman
2. **Implementasi scale recovery** menggunakan tinggi kamera
3. **Perhitungan diameter & kedalaman** dari depth map
4. **Testing dengan objek ukuran diketahui** untuk validasi

---

**Referensi:** BAB 3.4 Metodologi Penelitian - Kalibrasi Kamera
