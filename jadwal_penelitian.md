# JADWAL PENELITIAN SKRIPSI

## Sistem Informasi Cerdas untuk Deteksi, Estimasi Ukuran, dan Pelaporan Otomatis Jalan Berlubang Secara Real-time Menggunakan YOLOv8

**Peneliti:** Pangeran Juhrifar Jafar  
**NIM:** H071231056  
**Program Studi:** Sistem Informasi  
**Fakultas:** Matematika dan Ilmu Pengetahuan Alam  
**Universitas Hasanuddin**

---

## TIMELINE PENELITIAN (16 MINGGU)

### **FASE 1: PERSIAPAN DAN LITERATURE REVIEW** 
**Minggu 1-3 (3 minggu)**

#### **Minggu 1: Literature Review dan Studi Pendahuluan**
**Target:** Memahami state-of-the-art dan gap penelitian

**Aktivitas:**
- [ ] **Hari 1-2:** Studi literatur YOLOv8 untuk object detection
- [ ] **Hari 3-4:** Studi literatur DepthAnything V2 untuk depth estimation
- [ ] **Hari 5-7:** Analisis penelitian terdahulu tentang potholes detection

**Deliverables:**
- [ ] Summary paper YOLOv8 (2-3 halaman)
- [ ] Summary paper DepthAnything V2 (2-3 halaman)
- [ ] Analisis gap penelitian (1 halaman)

**Kriteria Evaluasi:**
- Pemahaman mendalam tentang teknologi yang digunakan
- Identifikasi gap penelitian yang jelas
- Dokumentasi referensi yang lengkap

---

#### **Minggu 2: Dataset Collection dan Environment Setup**
**Target:** Persiapan dataset dan environment development

**Aktivitas:**
- [ ] **Hari 1-2:** Download dan eksplorasi dataset Roboflow
- [ ] **Hari 3-4:** Setup environment Python, PyTorch, OpenCV
- [ ] **Hari 5-7:** Install dan konfigurasi YOLOv8, DepthAnything V2

**Deliverables:**
- [ ] Dataset Roboflow siap digunakan
- [ ] Environment development berfungsi
- [ ] Test run YOLOv8 dan DepthAnything V2

**Kriteria Evaluasi:**
- Dataset dapat diakses dan digunakan
- Environment berjalan tanpa error
- Model dapat melakukan inference dasar

---

#### **Minggu 3: Kalibrasi Kamera dan Hardware Preparation**
**Target:** Persiapan hardware dan kalibrasi kamera

**Aktivitas:**
- [ ] **Hari 1-2:** Pembelian dan setup hardware (GPU, kamera)
- [ ] **Hari 3-4:** Kalibrasi kamera menggunakan checkerboard
- [ ] **Hari 5-7:** Validasi parameter kalibrasi kamera

**Deliverables:**
- [ ] Hardware siap digunakan
- [ ] Parameter kalibrasi kamera (K, dist)
- [ ] Validasi kalibrasi dengan reprojection error < 0.5 pixel

**Kriteria Evaluasi:**
- Hardware berfungsi optimal
- Kalibrasi kamera akurat
- Parameter tersimpan dan terdokumentasi

---

### **FASE 2: IMPLEMENTASI MODEL DETECTION**
**Minggu 4-6 (3 minggu)**

#### **Minggu 4: YOLOv8 Training dan Fine-tuning**
**Target:** Model YOLOv8 terlatih untuk deteksi potholes

**Aktivitas:**
- [ ] **Hari 1-2:** Data preprocessing dan augmentation
- [ ] **Hari 3-4:** Transfer learning dari pre-trained weights
- [ ] **Hari 5-7:** Fine-tuning dan hyperparameter tuning

**Deliverables:**
- [ ] Model YOLOv8 terlatih (.pt file)
- [ ] Training logs dan metrics
- [ ] Validation results (mAP@0.5 > 0.8)

**Kriteria Evaluasi:**
- Model dapat mendeteksi potholes dengan akurasi tinggi
- Training loss konvergen
- Validation metrics memenuhi target

---

#### **Minggu 5: DepthAnything V2 Integration**
**Target:** Integrasi DepthAnything V2 untuk depth estimation

**Aktivitas:**
- [ ] **Hari 1-2:** Setup dan testing DepthAnything V2
- [ ] **Hari 3-4:** Integrasi dengan pipeline YOLOv8
- [ ] **Hari 5-7:** Optimasi untuk real-time processing

**Deliverables:**
- [ ] DepthAnything V2 terintegrasi
- [ ] Pipeline detection + depth estimation
- [ ] Performance benchmark (FPS > 15)

**Kriteria Evaluasi:**
- Depth map dihasilkan dengan kualitas baik
- Pipeline berjalan real-time
- Integrasi tidak menurunkan performa detection

---

#### **Minggu 6: Scale Recovery Implementation**
**Target:** Implementasi scale recovery untuk konversi metrik

**Aktivitas:**
- [ ] **Hari 1-2:** Implementasi height-based scale recovery
- [ ] **Hari 3-4:** Implementasi object-based scale recovery
- [ ] **Hari 5-7:** Validasi scale recovery dengan objek referensi

**Deliverables:**
- [ ] Scale recovery module
- [ ] Validasi dengan objek ukuran diketahui
- [ ] Error scale recovery < 3%

**Kriteria Evaluasi:**
- Scale recovery akurat untuk berbagai jarak
- Validasi dengan ground truth manual
- Error dalam toleransi yang dapat diterima

---

### **FASE 3: IMPLEMENTASI SISTEM TERINTEGRASI**
**Minggu 7-9 (3 minggu)**

#### **Minggu 7: Robust Statistics dan Pengukuran Ukuran**
**Target:** Implementasi pengukuran diameter dan kedalaman

**Aktivitas:**
- [ ] **Hari 1-2:** Implementasi robust statistics (median, percentile)
- [ ] **Hari 3-4:** Implementasi outlier removal (IQR method)
- [ ] **Hari 5-7:** Implementasi pengukuran diameter dan kedalaman

**Deliverables:**
- [ ] Robust statistics module
- [ ] Pengukuran diameter dan kedalaman
- [ ] Validasi dengan ground truth manual

**Kriteria Evaluasi:**
- Pengukuran stabil dan akurat
- Robust terhadap noise pada depth map
- Error pengukuran < 5% untuk diameter, < 10% untuk kedalaman

---

#### **Minggu 8: Object Tracking dan Temporal Filtering**
**Target:** Implementasi BoT-SORT dan Kalman Filter

**Aktivitas:**
- [ ] **Hari 1-2:** Implementasi BoT-SORT tracking
- [ ] **Hari 3-4:** Implementasi Kalman Filter untuk temporal filtering
- [ ] **Hari 5-7:** Integrasi tracking dan filtering dengan pipeline

**Deliverables:**
- [ ] BoT-SORT tracking module
- [ ] Kalman Filter untuk temporal smoothing
- [ ] Pipeline terintegrasi dengan tracking

**Kriteria Evaluasi:**
- Tracking ID konsisten antar frame
- Temporal filtering mengurangi noise
- Pipeline berjalan real-time dengan tracking

---

#### **Minggu 9: REST API dan Dashboard**
**Target:** Implementasi API dan dashboard untuk pelaporan

**Aktivitas:**
- [ ] **Hari 1-2:** Implementasi REST API menggunakan FastAPI
- [ ] **Hari 3-4:** Implementasi dashboard monitoring
- [ ] **Hari 5-7:** Integrasi API dengan pipeline deteksi

**Deliverables:**
- [ ] REST API endpoint untuk pelaporan
- [ ] Dashboard monitoring real-time
- [ ] Dokumentasi API

**Kriteria Evaluasi:**
- API dapat menerima dan mengirim data
- Dashboard menampilkan data real-time
- Integrasi berjalan tanpa error

---

### **FASE 4: VALIDASI DAN TESTING**
**Minggu 10-12 (3 minggu)**

#### **Minggu 10: Ablation Study dan Performance Testing**
**Target:** Evaluasi kontribusi setiap komponen

**Aktivitas:**
- [ ] **Hari 1-2:** Implementasi ablation study
- [ ] **Hari 3-4:** Performance testing pada dataset test
- [ ] **Hari 5-7:** Analisis hasil dan optimasi

**Deliverables:**
- [ ] Hasil ablation study
- [ ] Performance metrics lengkap
- [ ] Analisis kontribusi setiap komponen

**Kriteria Evaluasi:**
- Setiap komponen berkontribusi signifikan
- Performance metrics memenuhi target
- Analisis mendalam tentang trade-offs

---

#### **Minggu 11: Real-world Testing dan Validation**
**Target:** Testing pada kondisi real-world

**Aktivitas:**
- [ ] **Hari 1-2:** Pengambilan data real-world
- [ ] **Hari 3-4:** Testing sistem pada data real
- [ ] **Hari 5-7:** Validasi dengan ground truth manual

**Deliverables:**
- [ ] Dataset real-world testing
- [ ] Hasil validasi real-world
- [ ] Ground truth manual untuk validasi

**Kriteria Evaluasi:**
- Sistem berfungsi pada kondisi real-world
- Validasi dengan ground truth manual
- Error dalam toleransi yang dapat diterima

---

#### **Minggu 12: System Integration dan Optimization**
**Target:** Integrasi final dan optimasi performa

**Aktivitas:**
- [ ] **Hari 1-2:** Integrasi semua komponen
- [ ] **Hari 3-4:** Optimasi performa dan latensi
- [ ] **Hari 5-7:** Testing end-to-end pipeline

**Deliverables:**
- [ ] Sistem terintegrasi lengkap
- [ ] Optimasi performa
- [ ] Testing end-to-end berhasil

**Kriteria Evaluasi:**
- Semua komponen terintegrasi dengan baik
- Performa optimal untuk real-time
- Pipeline end-to-end berjalan stabil

---

### **FASE 5: ANALISIS DAN PENULISAN**
**Minggu 13-16 (4 minggu)**

#### **Minggu 13: Data Analysis dan Results Processing**
**Target:** Analisis hasil eksperimen dan validasi

**Aktivitas:**
- [ ] **Hari 1-2:** Analisis hasil ablation study
- [ ] **Hari 3-4:** Analisis hasil real-world testing
- [ ] **Hari 5-7:** Perbandingan dengan state-of-the-art

**Deliverables:**
- [ ] Analisis hasil eksperimen
- [ ] Perbandingan dengan baseline
- [ ] Kesimpulan dan insights

**Kriteria Evaluasi:**
- Analisis mendalam dan komprehensif
- Perbandingan objektif dengan baseline
- Insights yang valuable untuk penelitian

---

#### **Minggu 14: Penulisan Laporan dan Dokumentasi**
**Target:** Penulisan laporan penelitian

**Aktivitas:**
- [ ] **Hari 1-2:** Penulisan metodologi dan implementasi
- [ ] **Hari 3-4:** Penulisan hasil dan analisis
- [ ] **Hari 5-7:** Penulisan kesimpulan dan saran

**Deliverables:**
- [ ] Draft laporan penelitian
- [ ] Dokumentasi teknis lengkap
- [ ] User manual dan developer guide

**Kriteria Evaluasi:**
- Laporan lengkap dan terstruktur
- Dokumentasi teknis jelas
- User manual mudah dipahami

---

#### **Minggu 15: Review dan Revisi**
**Target:** Review dan revisi laporan

**Aktivitas:**
- [ ] **Hari 1-2:** Review laporan dengan pembimbing
- [ ] **Hari 3-4:** Revisi berdasarkan feedback
- [ ] **Hari 5-7:** Finalisasi laporan dan dokumentasi

**Deliverables:**
- [ ] Laporan yang telah direvisi
- [ ] Dokumentasi final
- [ ] Code repository yang terorganisir

**Kriteria Evaluasi:**
- Laporan sesuai standar akademik
- Feedback pembimbing diimplementasikan
- Dokumentasi lengkap dan terorganisir

---

#### **Minggu 16: Persiapan Presentasi dan Finalisasi**
**Target:** Persiapan presentasi dan finalisasi

**Aktivitas:**
- [ ] **Hari 1-2:** Persiapan presentasi final
- [ ] **Hari 3-4:** Rehearsal presentasi
- [ ] **Hari 5-7:** Finalisasi semua deliverables

**Deliverables:**
- [ ] Presentasi final
- [ ] Laporan final
- [ ] Semua deliverables siap

**Kriteria Evaluasi:**
- Presentasi siap dan terlatih
- Semua deliverables lengkap
- Siap untuk sidang skripsi

---

## **MILESTONE DAN DELIVERABLES**

### **Milestone Utama:**
1. **Minggu 3:** Environment dan dataset siap
2. **Minggu 6:** Model detection dan depth estimation siap
3. **Minggu 9:** Sistem terintegrasi siap
4. **Minggu 12:** Validasi dan testing selesai
5. **Minggu 16:** Laporan dan presentasi siap

### **Deliverables Utama:**
1. **Model YOLOv8** terlatih untuk deteksi potholes
2. **Sistem DepthAnything V2** terintegrasi
3. **Scale Recovery Module** untuk konversi metrik
4. **REST API** untuk pelaporan
5. **Dashboard** monitoring real-time
6. **Laporan Penelitian** lengkap
7. **Dokumentasi Teknis** dan user manual

---

## **KRITERIA EVALUASI**

### **Evaluasi Mingguan:**
- **Progress:** 80% aktivitas mingguan selesai
- **Quality:** Deliverables memenuhi standar
- **Timeline:** Sesuai jadwal yang direncanakan

### **Evaluasi Fase:**
- **Fase 1:** Environment dan dataset siap
- **Fase 2:** Model detection berfungsi
- **Fase 3:** Sistem terintegrasi lengkap
- **Fase 4:** Validasi dan testing selesai
- **Fase 5:** Laporan dan presentasi siap

### **Evaluasi Akhir:**
- **Teknis:** Sistem berfungsi sesuai spesifikasi
- **Akademik:** Laporan sesuai standar skripsi
- **Praktis:** Sistem dapat diimplementasikan

---

## **RISIKO DAN MITIGASI**

### **Risiko Teknis:**
- **Hardware tidak memadai:** Backup plan dengan cloud computing
- **Model tidak konvergen:** Hyperparameter tuning dan transfer learning
- **Integrasi gagal:** Modular development dan testing

### **Risiko Jadwal:**
- **Keterlambatan implementasi:** Parallel development dan prioritization
- **Testing memakan waktu:** Automated testing dan validation
- **Revisi laporan:** Buffer time dan early review

### **Risiko Kualitas:**
- **Akurasi rendah:** Data augmentation dan model tuning
- **Performance buruk:** Optimization dan profiling
- **Dokumentasi kurang:** Template dan checklist

---

## **RESOURCE REQUIREMENTS**

### **Hardware:**
- GPU RTX 3060 12GB (training dan inference)
- CPU Intel i7-12700K (preprocessing)
- RAM 32GB DDR4 (dataset besar)
- Storage 1TB NVMe SSD (fast I/O)

### **Software:**
- Python 3.8+
- PyTorch 2.0+
- OpenCV 4.8+
- Ultralytics YOLOv8
- DepthAnything V2
- FastAPI
- Docker

### **Dataset:**
- Roboflow Potholes Dataset
- RDD2022 Dataset (tambahan)
- COCO Dataset (pre-training)
- Data real-world (self-collected)

---

## **KOMITMEN PENELITI**

### **Waktu:**
- **40+ jam per minggu** untuk penelitian
- **Dedikasi penuh** selama 16 minggu
- **Konsistensi** dalam progress mingguan

### **Kualitas:**
- **Standar akademik** untuk semua deliverables
- **Dokumentasi lengkap** untuk setiap tahap
- **Testing menyeluruh** untuk setiap komponen

### **Kolaborasi:**
- **Feedback berkala** dengan pembimbing
- **Open communication** tentang challenges
- **Willingness to learn** teknologi baru

---

**Dokumen ini akan diupdate setiap minggu berdasarkan progress aktual dan feedback dari pembimbing.**
