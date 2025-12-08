# 📁 Struktur Proyek YOLOv8n Pothole Detection

## 🎯 Overview

Proyek ini telah diorganisir ulang untuk memisahkan:
- **Model training** (sudah selesai) → `runs/detect/.../weights/best.pt`
- **Source code** (sistem deteksi) → `src/`
- **Dokumentasi** → `panduan/`
- **Scripts & utilities** → Root & `utils/`

## 📂 Struktur Folder

```
Yolov8n/
│
├── src/                                    # ⭐ SOURCE CODE UTAMA
│   ├── __init__.py                        # Package initialization
│   ├── pothole_detection_system.py        # Main system (YOLO + Depth + Measurement)
│   ├── depth_estimation.py                # DepthAnything V2 integration
│   ├── pothole_tracker.py                 # BoT-SORT tracker
│   ├── kalman_filter.py                   # Kalman filter untuk temporal filtering
│   └── example_usage.py                   # Contoh penggunaan (module)
│
├── example_usage.py                       # Wrapper script (bisa dijalankan langsung)
│
├── runs/                                  # 📊 HASIL TRAINING
│   └── detect/
│       └── yolov8n-potholes-ft/
│           └── weights/
│               └── best.pt                # ⭐ MODEL YANG DIPAKAI
│
├── utils/                                 # 🔧 UTILITIES
│   └── camera_calibration.py             # Utility kalibrasi kamera
│
├── datasets/                              # 📦 DATASET
│   └── potholes_raw/                     # Dataset training
│
├── panduan/                               # 📚 DOKUMENTASI
│   ├── README_POTHOLE_SYSTEM.md         # Dokumentasi sistem utama
│   ├── NEXT_STEPS.md                     # Langkah selanjutnya
│   └── ...
│
├── test_yolo.py                          # Script testing
├── train_yolo.py                         # Script training
└── requirements.txt                      # Dependencies
```

## 🚀 Cara Menggunakan

### 1. Import dari Package

```python
# Method 1: Import langsung dari module
from src.pothole_detection_system import PotholeDetectionSystem

# Method 2: Import dari package (recommended)
from src import PotholeDetectionSystem, DepthEstimator, PotholeTracker
```

### 2. Jalankan Contoh

```bash
# Jalankan example_usage.py di root
python example_usage.py

# Atau jalankan sebagai module
python -m src.example_usage
```

### 3. Gunakan Model

```python
from src import PotholeDetectionSystem

system = PotholeDetectionSystem(
    yolo_model_path="runs/detect/yolov8n-potholes-ft/weights/best.pt",
    depth_model_type="small",
    camera_calib_path="camera_params.json",  # optional
    camera_height=1.5
)

# Process image
results = system.process_frame(image)
```

## 📝 File Penting

### ✅ Yang Dipakai untuk Inference:
- `runs/detect/yolov8n-potholes-ft/weights/best.pt` - **Model YOLO yang sudah terlatih**
- `src/pothole_detection_system.py` - Sistem utama
- `src/depth_estimation.py` - Estimasi kedalaman
- `src/pothole_tracker.py` - Tracking
- `src/kalman_filter.py` - Filtering temporal

### 📚 Dokumentasi:
- `panduan/README_POTHOLE_SYSTEM.md` - Dokumentasi lengkap sistem
- `panduan/NEXT_STEPS.md` - Langkah selanjutnya setelah training

### 🔧 Utilities:
- `utils/camera_calibration.py` - Kalibrasi kamera
- `example_usage.py` - Contoh penggunaan

## ⚠️ Catatan Penting

1. **Model `best.pt`** adalah file yang **paling penting** - ini hasil training yang digunakan untuk inference
2. **File `.py` di `src/`** adalah kode yang menjalankan sistem deteksi
3. **Keduanya diperlukan**: Model untuk deteksi, kode untuk menjalankan sistem
4. Struktur baru ini membuat proyek lebih rapi dan mudah di-maintain

## 🔄 Migrasi dari Struktur Lama

Jika Anda punya script yang menggunakan import lama:

**Sebelum:**
```python
from pothole_detection_system import PotholeDetectionSystem
```

**Sesudah:**
```python
from src.pothole_detection_system import PotholeDetectionSystem
# atau
from src import PotholeDetectionSystem
```

## 📖 Dokumentasi Lengkap

Lihat `panduan/README_POTHOLE_SYSTEM.md` untuk dokumentasi lengkap tentang:
- Instalasi dependencies
- Konfigurasi sistem
- Metodologi perhitungan
- Troubleshooting

