# 📋 TODO Checklist - Modifikasi Model YOLOv8
**Target Selesai: 9 November 2024** (16 hari dari sekarang)

## 🎯 **Fase 1: Kalibrasi & Setup (25-27 Oktober)**

### 📸 Kalibrasi Kamera
- [ ] **Ambil 15-30 foto checkerboard** dari berbagai sudut & jarak
  - [ ] Foto dari depan (0°)
  - [ ] Foto dari samping kiri (45°)
  - [ ] Foto dari samping kanan (45°)
  - [ ] Foto dari atas (90°)
  - [ ] Foto dari bawah (90°)
  - [ ] Foto dari jarak dekat (1 meter)
  - [ ] Foto dari jarak jauh (3 meter)
  - [ ] Foto dengan pencahayaan berbeda

- [ ] **Jalankan skrip kalibrasi OpenCV**
  - [ ] Install OpenCV dependencies
  - [ ] Run camera_calibration.py
  - [ ] Verifikasi hasil kalibrasi

- [ ] **Simpan hasil kalibrasi**
  - [ ] Simpan ke camera_calib.json
  - [ ] Format: camera_matrix + dist_coeffs
  - [ ] Test undistortion dengan sample image

## 🎯 **Fase 2: DepthAnything Integration (28-30 Oktober)**

### 🔧 Setup Environment
- [ ] **Install DepthAnything V2**
  - [ ] Clone repository DepthAnything
  - [ ] Install dependencies (torch, transformers, etc.)
  - [ ] Download pre-trained weights
  - [ ] Test inference dengan sample image

- [ ] **Integrasi dengan YOLOv8**
  - [ ] Load model YOLOv8 trained (best.pt)
  - [ ] Load DepthAnything V2 model
  - [ ] Buat pipeline: YOLOv8 → DepthAnything
  - [ ] Test dengan sample video/image

## 🎯 **Fase 3: Scale Recovery & Measurement (31 Okt - 2 Nov)**

### 📏 Scale Recovery Mechanism
- [ ] **Implementasi Scale Recovery**
  - [ ] Load camera calibration parameters
  - [ ] Implementasi height-based scale recovery
  - [ ] Konversi depth relatif ke absolut
  - [ ] Test dengan known distances

- [ ] **Perhitungan Diameter & Kedalaman**
  - [ ] Extract region dari detection mask
  - [ ] Analisis depth map di region pothole
  - [ ] Hitung diameter: (px × Z) / fx
  - [ ] Hitung kedalaman: Z_surface - Z_base

- [ ] **Robust Statistics**
  - [ ] Implementasi median filter
  - [ ] Implementasi IQR method untuk outlier removal
  - [ ] Test dengan noisy depth maps

## 🎯 **Fase 4: Temporal Filtering & Pipeline (3-5 November)**

### 🔄 Temporal Filtering
- [ ] **Kalman Filter Implementation**
  - [ ] Setup Kalman filter state (diameter, depth, velocity)
  - [ ] Implementasi predict step
  - [ ] Implementasi update step
  - [ ] Test dengan simulated noisy measurements

- [ ] **Object Tracking**
  - [ ] Integrasi BoT-SORT untuk tracking
  - [ ] Link tracking dengan Kalman filter
  - [ ] Test dengan video sequences

### 🔗 End-to-End Pipeline
- [ ] **Complete Pipeline**
  - [ ] YOLOv8 Detection → DepthAnything → Scale Recovery → Kalman Filter
  - [ ] Real-time processing optimization
  - [ ] API integration untuk reporting
  - [ ] Error handling dan logging

## 🎯 **Fase 5: Testing & Dokumentasi (6-9 November)**

### 🧪 Testing & Validation
- [ ] **Real-time Testing**
  - [ ] Test dengan video potholes
  - [ ] Measure processing speed (FPS)
  - [ ] Test accuracy dengan manual measurements
  - [ ] Test di berbagai kondisi lighting

- [ ] **Performance Metrics**
  - [ ] MAE diameter (target: <5cm)
  - [ ] MAE depth (target: <2cm)
  - [ ] Processing speed (target: >15 FPS)
  - [ ] Memory usage monitoring

### 📝 Dokumentasi
- [ ] **Laporan Modifikasi Model**
  - [ ] Dokumentasi arsitektur enhanced YOLOv8
  - [ ] Dokumentasi scale recovery mechanism
  - [ ] Dokumentasi temporal filtering
  - [ ] Code documentation dengan comments

- [ ] **Hasil & Analisis**
  - [ ] Comparison dengan baseline YOLOv8
  - [ ] Ablation study results
  - [ ] Real-world validation results
  - [ ] Screenshots dan demo video

## 📊 **Progress Tracking**

### Daily Progress
- **28 Oktober:** [ ] Kalibrasi kamera dimulai
- **29 Oktober:** [ ] Kalibrasi kamera selesai
- **30 Oktober:** [ ] Setup DepthAnything V2
- **31 Oktober:** [ ] Integrasi YOLOv8 + DepthAnything
- **1 November:** [ ] Scale recovery implementation
- **2 November:** [ ] Measurement calculation
- **3 November:** [ ] Robust statistics
- **4 November:** [ ] Kalman filter implementation
- **5 November:** [ ] Object tracking
- **6 November:** [ ] End-to-end pipeline
- **7 November:** [ ] Testing & optimization
- **8 November:** [ ] Final testing
- **9 November:** [ ] Dokumentasi selesai

### Key Milestones
- [ ] **30 Oktober:** Kalibrasi kamera selesai
- [ ] **2 November:** DepthAnything integration selesai
- [ ] **5 November:** Scale recovery & measurement selesai
- [ ] **8 November:** Temporal filtering & pipeline selesai
- [ ] **9 November:** Testing & dokumentasi selesai

## 🎯 **Success Criteria**

### Technical Requirements
- [ ] **Detection Accuracy:** mAP@0.5 > 0.80
- [ ] **Measurement Accuracy:** MAE diameter < 5cm, MAE depth < 2cm
- [ ] **Real-time Performance:** >15 FPS pada RTX 3060
- [ ] **Integration:** End-to-end pipeline berfungsi
- [ ] **Documentation:** Complete technical documentation

### Deliverables
- [ ] **Enhanced YOLOv8 Model** dengan depth estimation
- [ ] **Scale Recovery Implementation** untuk absolute measurements
- [ ] **Temporal Filtering System** dengan Kalman filter
- [ ] **Complete Pipeline** dari detection ke measurement
- [ ] **Technical Report** modifikasi model YOLOv8
- [ ] **Demo Video** real-time pothole detection & measurement

---

**📅 Target Deadline: 9 November 2024**  
**🎯 Status: Ready to Start!**  
**⚡ Next Action: Mulai kalibrasi kamera**
