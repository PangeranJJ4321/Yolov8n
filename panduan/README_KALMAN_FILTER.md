# Kalman Filter untuk Temporal Filtering (FASE 6)

## Overview

Kalman Filter diimplementasikan untuk menghaluskan fluktuasi pengukuran diameter dan depth lintas frame. Filter ini menggunakan constant velocity model untuk memprediksi dan memperbarui state measurements.

## Arsitektur

### State Vector
```
x = [diameter, depth, velocity_diameter, velocity_depth]^T
```

### Measurement Vector
```
z = [diameter, depth]^T
```

### State Transition Model (Constant Velocity)
```
x_k = F * x_{k-1}

F = [1  0  dt  0 ]
    [0  1  0  dt]
    [0  0  1   0 ]
    [0  0  0   1 ]
```

### Observation Model
```
z = H * x

H = [1  0  0  0]
    [0  1  0  0]
```

## Implementasi

### Class: `MeasurementKalmanFilter`

**File:** `kalman_filter.py`

**Methods:**
- `initialize(diameter, depth)`: Initialize filter dengan measurement pertama
- `predict()`: Prediction step berdasarkan model
- `update(diameter, depth)`: Update step dengan measurement baru
- `get_filtered_measurements()`: Get filtered diameter & depth
- `get_uncertainty()`: Get uncertainty (standard deviation)

**Parameters:**
- `process_noise` (Q): Seberapa cepat state berubah
  - Tinggi: filter lebih responsif, kurang smooth
  - Rendah: filter lebih smooth, kurang responsif
  - Default: 0.1
- `measurement_noise` (R): Seberapa percaya pada measurement
  - Tinggi: kurang percaya measurement, lebih smooth
  - Rendah: lebih percaya measurement, kurang smooth
  - Default: 1.0

## Integrasi dengan Tracker

Kalman Filter terintegrasi otomatis dengan `PotholeTracker`:

```python
from pothole_detection_system import PotholeDetectionSystem

system = PotholeDetectionSystem(
    yolo_model_path="path/to/model.pt",
    enable_tracking=True,  # Kalman filter otomatis enabled
    # Kalman parameters (optional)
    # kalman_process_noise=0.1,
    # kalman_measurement_noise=1.0
)
```

Setiap `Track` object memiliki instance `MeasurementKalmanFilter` yang:
1. Di-initialize saat track dibuat
2. Di-update setiap kali track mendapat detection baru
3. Di-predict saat track tidak mendapat detection (lost track)

## Penggunaan

### Basic Usage

```python
from kalman_filter import MeasurementKalmanFilter

# Initialize
kf = MeasurementKalmanFilter(
    initial_diameter=45.0,
    initial_depth=10.0,
    process_noise=0.1,
    measurement_noise=1.0
)

# Update dengan measurement baru
filtered_d, filtered_h = kf.update(noisy_diameter, noisy_depth)

# Get filtered values
filtered_d, filtered_h = kf.get_filtered_measurements()
```

### Dengan PotholeDetectionSystem

```python
from pothole_detection_system import PotholeDetectionSystem

system = PotholeDetectionSystem(
    yolo_model_path="model.pt",
    enable_tracking=True  # Kalman filter otomatis aktif
)

# Process frame
results = system.process_frame(image)

# Access filtered measurements dari tracks
for track in results['tracks']:
    filtered_d, filtered_h = track.get_filtered_measurements()
    print(f"Track {track.track_id}: D={filtered_d:.1f}cm, H={filtered_h:.1f}cm")
```

## Tuning Parameters

### Process Noise (Q)
- **0.01 - 0.05**: Sangat smooth, kurang responsif (baik untuk measurements yang sangat stabil)
- **0.1 - 0.2**: Balance (default recommended)
- **0.5 - 1.0**: Sangat responsif, kurang smooth (baik untuk measurements yang berubah cepat)

### Measurement Noise (R)
- **0.5 - 1.0**: Percaya pada measurement (default recommended)
- **2.0 - 5.0**: Kurang percaya, lebih smooth (baik untuk noisy measurements)
- **10.0+**: Sangat smooth, hampir ignore measurements (tidak recommended)

### Grid Search untuk Tuning

```python
import numpy as np
from kalman_filter import MeasurementKalmanFilter

# Test different parameters
process_noises = [0.05, 0.1, 0.2, 0.5]
measurement_noises = [0.5, 1.0, 2.0, 5.0]

best_params = None
best_rmse = float('inf')

for q in process_noises:
    for r in measurement_noises:
        kf = MeasurementKalmanFilter(process_noise=q, measurement_noise=r)
        # Test dengan ground truth data
        rmse = test_kalman_filter(kf, ground_truth_data)
        if rmse < best_rmse:
            best_rmse = rmse
            best_params = (q, r)

print(f"Best params: Q={best_params[0]}, R={best_params[1]}, RMSE={best_rmse:.2f}")
```

## Testing

Run test script untuk melihat efek filtering:

```bash
python test_kalman_filter.py
```

Script ini akan:
1. Generate simulated noisy measurements
2. Apply Kalman filter
3. Visualize comparison (raw vs filtered)
4. Calculate statistics (std reduction)

## Output

### Visualisasi
- Raw measurements ditampilkan dengan label "(KF)" untuk filtered values
- Track age ditampilkan untuk menunjukkan stabilitas

### JSON Output
Measurements yang di-save ke JSON include:
- `is_filtered: true`: Indikator bahwa values sudah di-filter
- `diameter_cm`: Filtered diameter
- `depth_cm`: Filtered depth

## Keuntungan

1. **Stabilisasi**: Mengurangi fluktuasi noise pada measurements
2. **Outlier Rejection**: Filter secara otomatis mengurangi efek outliers
3. **Prediction**: Dapat memprediksi measurements saat track hilang sementara
4. **Uncertainty Estimation**: Menyediakan estimasi uncertainty untuk setiap measurement

## Limitations

1. **Constant Velocity Assumption**: Mengasumsikan perubahan measurements mengikuti constant velocity model
2. **Tuning Required**: Perlu tuning parameters untuk optimal performance
3. **Initialization**: Perlu beberapa frames untuk filter stabil (biasanya 5-10 frames)

## Referensi

- Kalman Filter Theory: [Wikipedia](https://en.wikipedia.org/wiki/Kalman_filter)
- Constant Velocity Model: Standard Kalman Filter implementation
- Tuning Guide: Grid search dengan ground truth validation

