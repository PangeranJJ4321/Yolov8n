# 🕳️ Pothole Detection System

Sistem terintegrasi untuk deteksi dan pengukuran pothole menggunakan YOLOv8 + DepthAnything V2.

## 📋 Overview

Sistem ini menggabungkan:
- **YOLOv8**: Deteksi pothole dengan bounding box
- **DepthAnything V2**: Estimasi kedalaman per-frame
- **Scale Recovery**: Konversi depth relatif ke absolut (meter)
- **Measurement**: Perhitungan diameter & kedalaman pothole

## 🏗️ Pipeline Lengkap

```
Input Video Frame
    ↓
┌─────────────────────┐
│  Undistort Image    │ ← Hapus distorsi lens
└─────────────────────┘
    ↓
┌─────────────────────┐
│  YOLOv8 Detection   │ → Bounding Box
└─────────────────────┘
    ↓
┌─────────────────────┐
│ DepthAnything V2    │ → Depth Map (relatif)
└─────────────────────┘
    ↓
┌─────────────────────┐
│  Scale Recovery     │ → Depth Map (absolut)
└─────────────────────┘
    ↓
┌──────────────────────────────────────────┐
│  Perhitungan Ukuran                      │
├──────────────────────────────────────────┤
│  1. Z_surface = median depth di border   │
│  2. Z_base = percentile 10% depth di ROI │
│  3. Outlier removal (IQR method)        │
│  4. Diameter = (width_px × Z_avg) / fx   │
│  5. Depth = Z_surface - Z_base           │
└──────────────────────────────────────────┘
    ↓
Output: Diameter & Depth (cm)
```

## 📦 Instalasi

### Dependencies

```bash
# Dependencies dasar
pip install opencv-python numpy torch torchvision ultralytics

# DepthAnything V2
pip install depth-anything-v2
# atau clone dari GitHub
git clone https://github.com/DepthAnything/Depth-Anything-V2.git
cd Depth-Anything-V2
pip install -e .
```

### File yang Diperlukan

1. **YOLO Model**: `runs/detect/yolov8n-potholes-ft/weights/best.pt`
2. **Camera Calibration**: `camera_params.json` (optional, untuk akurasi lebih baik)

## 🚀 Quick Start

### 1. Single Image Processing

```python
from pothole_detection_system import PotholeDetectionSystem
import cv2

# Initialize system
system = PotholeDetectionSystem(
    yolo_model_path="runs/detect/yolov8n-potholes-ft/weights/best.pt",
    depth_model_type="small",
    camera_calib_path="camera_params.json",  # optional
    camera_height=1.5,  # tinggi kamera dari jalan (meter)
    conf_threshold=0.25
)

# Load dan process image
image = cv2.imread("path/to/image.jpg")
results = system.process_frame(image)

# Print results
for i, measurement in enumerate(results['measurements']):
    print(f"Pothole {i+1}:")
    print(f"  Diameter: {measurement.diameter_cm:.2f} cm")
    print(f"  Depth: {measurement.depth_cm:.2f} cm")
    print(f"  Confidence: {measurement.confidence:.3f}")

# Visualize
vis_image = system.visualize_results(image, results)
cv2.imwrite("output/result.jpg", vis_image)
```

### 2. Video Processing

```python
# Process video
summary = system.process_video(
    video_path="path/to/video.mp4",
    output_path="output/detected_video.avi",
    show_preview=False,
    frame_skip=1,  # Process setiap frame
    save_measurements=True  # Simpan ke JSON
)

print(f"Total detections: {summary['total_detections']}")
print(f"Measurements saved: {summary['measurements_file']}")
```

## 📊 Output Format

### PotholeMeasurement Object

```python
class PotholeMeasurement:
    bbox: Tuple[int, int, int, int]  # (x1, y1, x2, y2)
    confidence: float                 # YOLO confidence
    diameter_cm: float                # Diameter dalam cm
    depth_cm: float                   # Kedalaman dalam cm
    z_surface: float                  # Z surface (meter)
    z_base: float                     # Z base (meter)
    z_avg: float                      # Z average (meter)
    mask: Optional[np.ndarray]        # Segmentation mask (optional)
```

### JSON Output (Video Processing)

```json
[
  {
    "frame": 0,
    "bbox": [100, 200, 300, 400],
    "confidence": 0.85,
    "diameter_cm": 45.2,
    "depth_cm": 10.5,
    "z_surface_m": 1.45,
    "z_base_m": 1.35,
    "z_avg_m": 1.40
  },
  ...
]
```

## 🔧 Konfigurasi

### Parameter Penting

- **camera_height**: Tinggi kamera dari permukaan jalan (meter)
  - Penting untuk scale recovery
  - Ukur dengan akurat untuk hasil terbaik

- **conf_threshold**: Confidence threshold untuk YOLO
  - Default: 0.25
  - Naikkan untuk mengurangi false positives
  - Turunkan untuk meningkatkan recall

- **depth_model_type**: Tipe model DepthAnything
  - `"small"`: Cepat, akurasi sedang (recommended)
  - `"base"`: Seimbang
  - `"large"`: Lambat, akurasi tinggi

### Tanpa Kalibrasi Kamera

Jika kalibrasi tidak tersedia, sistem tetap bisa berjalan dengan depth relatif:

```python
system = PotholeDetectionSystem(
    yolo_model_path="best.pt",
    depth_model_type="small",
    camera_calib_path=None,  # Tanpa kalibrasi
    camera_height=1.5
)
```

⚠️ **Note**: Tanpa kalibrasi, diameter & depth akan dalam satuan relatif, bukan absolut.

## 📐 Metodologi Perhitungan

### 1. Z_surface (Permukaan Jalan)

- Menggunakan **median** dari border pixels (robust terhadap outlier)
- Border width: 10 pixels (default)

### 2. Z_base (Dasar Lubang)

- Menggunakan **percentile 10%** dari ROI depth
- Outlier removal dengan **IQR method**:
  - Q1 = percentile 25%
  - Q3 = percentile 75%
  - IQR = Q3 - Q1
  - Filter: [Q1 - 1.5×IQR, Q3 + 1.5×IQR]

### 3. Diameter

- **Dengan mask**: Fit ellipse pada contour, gunakan major axis
- **Tanpa mask**: Gunakan bounding box width
- Formula: `diameter_cm = (width_px × Z_avg × 100) / fx`

### 4. Depth

- Formula: `depth_cm = (Z_surface - Z_base) × 100`

## 🎯 Contoh Penggunaan Lengkap

Lihat file `example_usage.py` untuk contoh lengkap:
- Single image processing
- Video processing
- Step-by-step processing

## 📁 Struktur File

```
Yolov8n/
├── pothole_detection_system.py  # Main system class
├── depth_estimation.py           # DepthEstimator class
├── example_usage.py              # Contoh penggunaan
├── camera_calibration.py         # Utility kalibrasi
└── README_POTHOLE_SYSTEM.md     # Dokumentasi ini
```

## ⚠️ Troubleshooting

### 1. Import Error: depth_estimation module not found
- Pastikan `depth_estimation.py` ada di folder yang sama
- Atau tambahkan path ke `sys.path`

### 2. CUDA out of memory
- Gunakan `depth_model_type="small"`
- Kurangi resolusi input
- Gunakan `frame_skip > 1` untuk video

### 3. Measurements tidak akurat
- Pastikan kalibrasi kamera sudah benar
- Sesuaikan `camera_height` dengan tinggi sebenarnya
- Periksa apakah depth map ter-generate dengan baik

### 4. Tidak ada detections
- Turunkan `conf_threshold`
- Pastikan model YOLO sudah terlatih dengan baik
- Periksa input image/video

## 🔜 Next Steps (Fase Berikutnya)

1. **BoT-SORT Tracker**: Tracking pothole lintas frame
2. **Kalman Filter**: Stabilisasi pengukuran temporal
3. **API Integration**: Export hasil ke API/database

## 📝 Catatan

- Sistem ini adalah **FASE 4** dari pipeline lengkap
- Tracking dan temporal filtering akan ditambahkan di fase berikutnya
- Untuk akurasi maksimal, pastikan kalibrasi kamera sudah dilakukan

## 📚 Referensi

- YOLOv8: https://github.com/ultralytics/ultralytics
- DepthAnything V2: https://github.com/DepthAnything/Depth-Anything-V2
- Metodologi berdasarkan: Wang et al. (2025)

