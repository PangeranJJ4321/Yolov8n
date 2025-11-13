
## Sistem Informasi Cerdas untuk Deteksi, Estimasi Ukuran, dan Pelaporan Otomatis Jalan Berlubang Secara Real-time Menggunakan YOLOv8

**Disusun oleh:** Pangeran Juhrifar Jafar  
**NIM:** H071231056  
**Jurusan:** Sistem Informasi  
**Pembimbing:** Pak Supri

---

## BAB 1: PENDAHULUAN

### 1.1 Latar Belakang

Jalan merupakan infrastruktur vital yang menopang konektivitas dan pertumbuhan ekonomi. Namun, kualitas jalan seringkali terdegradasi oleh munculnya lubang (*potholes*), yang menjadi isu krusial berdampak negatif pada keselamatan lalu lintas, kenyamanan berkendara, dan peningkatan biaya perawatan kendaraan. Kerusakan ini dapat menyebabkan kecelakaan fatal dan kerugian material yang signifikan.

Metode deteksi konvensional yang diterapkan saat ini, seperti laporan manual dari warga dan inspeksi lapangan oleh pihak berwenang, memiliki berbagai kelemahan. Proses ini bersifat lambat, tidak efisien, subjektif, dan seringkali tidak akurat dalam skala besar. Keterlambatan dalam identifikasi dan penanganan menyebabkan kerusakan kecil berkembang menjadi kerusakan parah, yang pada akhirnya meningkatkan biaya perbaikan.

Untuk mengatasi tantangan ini, diperlukan sebuah sistem cerdas yang mampu bekerja secara otomatis. Kemajuan dalam bidang *Deep Learning*, khususnya pada model deteksi objek seperti **YOLOv8**, menawarkan solusi yang menjanjikan. YOLOv8 memungkinkan deteksi objek dengan akurasi tinggi dan performa *real-time*, sehingga sangat cocok untuk implementasi di dunia nyata, misalnya pada kendaraan yang bergerak.

Lebih dari sekadar mendeteksi, informasi kuantitatif mengenai dimensi lubang—seperti **diameter dan kedalaman**—sangatlah krusial. Data ini memungkinkan pihak berwenang untuk mengklasifikasikan tingkat keparahan kerusakan (misalnya, ringan, sedang, berat) dan menyusun prioritas perbaikan secara lebih efektif dan berbasis data.

Dengan mengintegrasikan hasil deteksi dan pengukuran ini ke dalam sebuah sistem pelaporan otomatis melalui **API (*Application Programming Interface*)**, informasi dapat dikirimkan secara langsung ke *dashboard* pemerintah. Hal ini akan mentransformasi model pemeliharaan jalan dari reaktif menjadi proaktif, mewujudkan sistem yang lebih cerdas, responsif, dan efisien.

### 1.2 Rumusan Masalah

1. Bagaimana merancang dan mengimplementasikan model **YOLOv8** untuk dapat mendeteksi jalan berlubang secara akurat dan *real-time* dari input video kamera dalam berbagai kondisi jalan?
2. Bagaimana mengembangkan metode untuk mengestimasi **diameter (2D)** dan **kedalaman (3D)** lubang secara akurat dan simultan dari citra kamera monokular dengan mengatasi tantangan skala absolut pada depth estimation?
3. Bagaimana merancang arsitektur sistem yang dapat mengirimkan data hasil deteksi (koordinat GPS, ukuran, *timestamp*) secara otomatis melalui **REST API** ke sebuah *dashboard* pemantauan?

### 1.3 Tujuan Penelitian

1. Mengimplementasikan sistem deteksi jalan berlubang secara *real-time* menggunakan model YOLOv8 (varian ringan seperti YOLOv8n atau YOLOv8s untuk latensi rendah).
2. Mengembangkan metode terintegrasi untuk mengestimasi **diameter** dan **kedalaman** lubang secara simultan menggunakan estimasi kedalaman monokular berbasis deep learning (DepthAnything V2) dengan penerapan **scale recovery** untuk akurasi metrik absolut.
3. Mengimplementasikan sistem pelacakan objek (BoT-SORT) dan pemfilteran temporal (Kalman Filter) untuk meningkatkan stabilitas dan akurasi pengukuran.
4. Menerapkan teknik **robust statistics** (median, percentile, outlier removal) untuk mengatasi noise pada depth map.
5. Merancang dan membuat prototipe **REST API** untuk mengirimkan data hasil deteksi ke sebuah *dashboard* simulasi pihak berwenang.

### 1.4 Manfaat Penelitian

1. **Bagi Pemerintah/Otoritas Jalan:** Menyediakan alat bantu pengambilan keputusan yang berbasis data *real-time* untuk pemeliharaan jalan yang lebih efisien, proaktif, dan terukur dengan klasifikasi severity otomatis.
2. **Bagi Masyarakat:** Meningkatkan keselamatan dan kenyamanan berkendara dengan mempercepat proses identifikasi dan perbaikan jalan yang rusak.
3. **Bagi Akademisi:** Memberikan kontribusi berupa prototipe sistem *end-to-end* dengan analisis mendalam tentang tantangan implementasi depth estimation monokular, solusi scale recovery, dan best practices untuk aplikasi real-world.

---

## BAB 2: TINJAUAN PUSTAKA DAN LANDASAN TEORI

### 2.1 Deteksi Jalan Berlubang

Deteksi jalan berlubang telah menjadi fokus penelitian di bidang visi komputer dan rekayasa transportasi. Metode awal meliputi analisis berbasis fitur citra, seperti tekstur, bentuk, dan warna. Namun, metode ini seringkali tidak andal dalam kondisi pencahayaan dan cuaca yang bervariasi.

Perkembangan *Deep Learning*, khususnya *Convolutional Neural Networks* (CNN), telah merevolusi bidang ini. Arsitektur seperti YOLO (*You Only Look Once*) menjadi standar karena kemampuannya memproses gambar dalam satu kali inferensi, sehingga sangat cepat dan cocok untuk aplikasi *real-time*.

**YOLOv5 & YOLOv8:** Penelitian oleh Hoseini et al. (2024) dan Gorro et al. (2024) secara spesifik menunjukkan keberhasilan penggunaan YOLOv5 dan YOLOv8 untuk deteksi jalan berlubang. Gorro et al. (2024) menekankan pentingnya augmentasi data, seperti *exposure bounding box* dan rotasi, untuk meningkatkan ketahanan model terhadap *overfitting* dan variasi kondisi dunia nyata.

### 2.2 Estimasi Ukuran dari Citra Menggunakan Deep Learning Monokular

#### 2.2.1 Pendekatan Terintegrasi untuk Diameter dan Kedalaman

**Wang et al. (2025)** merancang sebuah sistem utuh yang menggabungkan estimasi kedalaman menggunakan DepthAnything V2 (berbasis Dense Prediction Transformer), pelacakan objek dengan BoT-SORT, dan pemfilteran temporal menggunakan Kalman Filter (CDKF) untuk meningkatkan kekokohan pengukuran dari video. Pendekatan ini memungkinkan pengukuran diameter dan kedalaman secara simultan dari satu pipeline pemrosesan.

#### 2.2.2 Tantangan Depth Estimation Monokular

**Masalah Skala Absolut:** Salah satu tantangan utama dalam depth estimation monokular adalah bahwa sebagian besar model deep learning hanya menghasilkan kedalaman relatif (up-to-scale), bukan kedalaman absolut dalam satuan metrik. Hal ini terjadi karena model dilatih pada dataset dengan skala yang bervariasi dan tidak memiliki informasi tentang ukuran fisik sebenarnya dari objek dalam scene.

**Scale Ambiguity:** Tanpa informasi tambahan, tidak mungkin untuk membedakan antara objek kecil yang dekat dengan objek besar yang jauh, karena keduanya dapat menghasilkan proyeksi yang sama pada image plane.

#### 2.2.3 Model Pinhole Camera untuk Konversi Metrik

Dengan menggunakan depth map yang dihasilkan oleh model deep learning, ukuran piksel pada bounding box dapat dikonversi menjadi ukuran metrik di dunia nyata menggunakan model proyeksi pinhole camera. Metode ini memerlukan parameter intrinsik kamera (focal length, principal point) yang diperoleh melalui kalibrasi kamera standar menggunakan checkerboard pattern.

#### 2.2.4 Stabilisasi Temporal untuk Akurasi

Berbeda dengan pendekatan single-frame yang rentan noise, metode ini memanfaatkan informasi temporal dari rangkaian frame video. Kalman Filter digunakan untuk menghaluskan fluktuasi pengukuran antar frame, menghasilkan estimasi yang lebih stabil dan andal untuk aplikasi real-time.

### 2.3 Arsitektur Sistem Real-time

Untuk aplikasi *real-time* di kendaraan, pemrosesan harus dilakukan pada perangkat dengan sumber daya terbatas (*edge devices*). Platform seperti **NVIDIA Jetson** atau **Google Coral** sering digunakan untuk mengakselerasi inferensi model *deep learning*. Guan et al. (2025) mendemonstrasikan kelayakan ini dengan melakukan eksperimen di kendaraan menggunakan platform Jetson Xavier NX.

---

## BAB 3: METODOLOGI PENELITIAN

### 3.1 Pengumpulan dan Anotasi Dataset

**Sumber Data:**
- Dataset publik (Kaggle, RDD2022) sebagai data dasar
- Pengambilan data lokal menggunakan *dashcam* atau kamera ponsel untuk variasi kondisi Indonesia

**Anotasi:**
- Menggunakan **LabelImg** atau **Roboflow** untuk membuat *bounding box*
- **Preferensi:** Instance segmentation mask (YOLOv8-seg) untuk akurasi area lubang yang lebih presisi dibanding bbox rectangular
- Label: "lubang" (*pothole*)

**Metadata:**
- *Timestamp*, koordinat GPS, file kalibrasi intrinsik kamera
- **Tambahan:** Ground truth manual untuk diameter dan kedalaman (pengukuran lapangan dengan meteran/depth gauge) untuk validasi

**Data split:** Train / Val / Test (70/15/15)


### 3.2 Pra-pemrosesan & Augmentasi Data

**Undistortion:** Sebelum inferensi, lakukan undistortion menggunakan parameter kalibrasi untuk menghilangkan distorsi radial dan tangensial

**Ukuran Input:** 640×640 piksel untuk YOLOv8

**Teknik Augmentasi:**
- **Geometris:** *Horizontal flip*, rotasi, *random crop*, *cutout*
- **Fotometris:** Kecerahan, kontras, saturasi, *blur*
- **Tujuan:** Mengatasi ketidakseimbangan kelas dan simulasi kondisi nyata (siang, malam, hujan)

### 3.3 Pelatihan Model Deteksi (YOLOv8)

- **Model:** YOLOv8n atau YOLOv8s (ringan, cepat) dengan opsi YOLOv8-seg untuk instance segmentation
- **Transfer Learning:** Dari bobot COCO, *fine-tuning* pada dataset lubang
- **Optimasi:** Tuning *learning rate*, *batch size*, *epoch*
- **Regularisasi:** *Early stopping*, *weight decay*
- **Post-processing:** Tuning threshold non-max suppression

### 3.4 Kalibrasi Kamera (Tahap Kritis)

**Tujuan:** Mendapatkan parameter intrinsik kamera untuk konversi piksel ke metrik yang akurat.

**Langkah-langkah Detail:**

1. **Persiapan Checkerboard Pattern:**
   - Gunakan papan catur dengan ukuran kotak yang diketahui secara presisi (misal: 25mm × 25mm)
   - Cetak dengan printer berkualitas tinggi atau gunakan board profesional
   - Pastikan pattern datar (tidak melengkung)

2. **Pengambilan Gambar Kalibrasi:**
   - Ambil 15-20 foto checkerboard dari berbagai sudut dan jarak
   - Variasi posisi: kiri, kanan, atas, bawah, center, diagonal
   - Variasi jarak: dekat, sedang, jauh
   - Pastikan seluruh area checkerboard terlihat jelas di setiap foto

3. **Proses Kalibrasi dengan OpenCV:**
   ```python
   ret, K, dist, rvecs, tvecs = cv2.calibrateCamera(
       object_points, image_points, image_size, None, None
   )
   ```
   
4. **Output Parameter:**
   - **Matriks Intrinsik K:**
     ```
     K = [[fx,  0, cx],
          [ 0, fy, cy],
          [ 0,  0,  1]]
     ```
     - `fx`, `fy`: focal length dalam satuan piksel
     - `cx`, `cy`: principal point (biasanya mendekati pusat image)
   
   - **Koefisien Distorsi:** `dist = [k1, k2, p1, p2, k3]`
     - `k1, k2, k3`: radial distortion
     - `p1, p2`: tangential distortion

5. **Validasi Kalibrasi:**
   - Hitung reprojection error (harus < 0.5 piksel)
   - Visualisasi undistorted images
   - Test dengan objek ukuran diketahui

**Metadata yang Disimpan:**
- Matriks K dan dist dalam file JSON/YAML
- Informasi kamera: model, resolusi, tanggal kalibrasi
- Tinggi mounting kamera dari permukaan jalan (untuk scale recovery)
- Sudut pitch dan roll kamera (untuk road plane correction)

### 3.5 Metodologi Estimasi Diameter dan Kedalaman (Terintegrasi dengan Scale Recovery)

Penelitian ini menggunakan pendekatan monokular terintegrasi yang diadaptasi dari **Wang et al. (2025)** dengan penambahan komponen **scale recovery** dan **robust statistics** untuk mengatasi tantangan yang telah diidentifikasi dalam analisis.

#### 3.5.1 Setup Perangkat Keras

Hanya memerlukan **satu kamera** (dashcam atau kamera ponsel), membuatnya sangat praktis untuk diimplementasikan.

#### 3.5.2 Pipeline Pemrosesan Terintegrasi dengan Scale Recovery

**Alur Kerja Lengkap:**

```
Input Video Frame
    ↓
┌─────────────────────┐
│  Undistort Image    │ ← Hapus distorsi lens
└─────────────────────┘
    ↓
┌─────────────────────┐
│  YOLOv8 Detection   │ → Bounding Box / Segmentation Mask
└─────────────────────┘
    ↓
┌─────────────────────┐
│ DepthAnything V2    │ → Depth Map (relatif)
└─────────────────────┘
    ↓
┌─────────────────────┐
│  Scale Recovery     │ → Konversi depth relatif ke absolut
│  (Height-based)     │
└─────────────────────┘
    ↓
┌──────────────────────────────────────────┐
│  Ekstraksi Region & Perhitungan Ukuran  │
├──────────────────────────────────────────┤
│  1. Z_surface = median depth di border   │
│  2. Z_base = percentile 10% depth di ROI │
│  3. Outlier removal (IQR method)         │
│  4. Diameter = (width_px × Z_avg) / fx   │
│  5. Depth = Z_surface - Z_base           │
└──────────────────────────────────────────┘
    ↓
┌─────────────────────┐
│   BoT-SORT Tracker  │ → ID konsisten per lubang
└─────────────────────┘
    ↓
┌─────────────────────┐
│   Kalman Filter     │ → Stabilisasi pengukuran
│      (CDKF)         │    (diameter & depth)
└─────────────────────┘
    ↓
Output: Diameter & Depth metrik stabil
```

Catatan satuan dan konsistensi:
- Gunakan meter (m) untuk Z_surface, Z_base, Z_avg; piksel (px) untuk dimensi gambar; `fx` dalam piksel.
- Konversi eksplisit ke sentimeter (cm) hanya saat pelaporan (mis. `× 100`).

#### 3.5.3 Detail Implementasi per Komponen

**A. Estimasi Kedalaman per Frame**

- **Model:** DepthAnything V2 dengan arsitektur Dense Prediction Transformer (DPT)
- **Input:** Frame RGB undistorted (640×480 atau 1280×720)
- **Output:** Depth map dengan nilai kedalaman relatif (d_rel) untuk setiap piksel
- **Karakteristik:** Model menghasilkan depth up-to-scale, perlu scale factor S untuk konversi ke metrik

**B. Scale Recovery (Tahap Kritis Baru)**

**Masalah:** DepthAnything V2 menghasilkan depth relatif (d_rel), bukan absolut (d_abs).

**Solusi 1: Height-Based Scale Recovery (Metode Utama)**

Memanfaatkan tinggi mounting kamera yang diketahui sebagai referensi:

1. **Setup:**
   - Ukur tinggi kamera H dari permukaan jalan (misal: H = 1.5 meter)
   - Identifikasi area jalan datar di depan kamera dalam frame

2. **Perhitungan Scale Factor:**
   - Ambil region jalan datar (ROI_road)
   - Hitung median depth relatif: `d_rel_road = median(depth_map[ROI_road])`
   - Gunakan geometri pinhole camera:
     ```
    d_abs_road = H / sin(pitch_angle)
     scale_factor S = d_abs_road / d_rel_road
     ```
   - Untuk setiap piksel: `d_abs = S × d_rel`
   - Jika pitch sangat kecil (~0°) dan `sin(pitch)` tidak stabil, gunakan estimasi road-plane/homography untuk derivasi skala.

3. **Update Scale Dynamically:**
   - Lakukan scale recovery setiap N frame atau saat perubahan scene
   - Gunakan moving average untuk S agar stabil

**Solusi 2: Object-Based Scale Recovery (Backup/Validasi)**

Menggunakan objek dengan ukuran diketahui sebagai referensi:

1. **Marker Referensi:**
   - Garis jalan (lebar standar: 10-15 cm)
   - Manhole cover (diameter standar: 60 cm)
   - Road marker/rambu dengan ukuran diketahui

2. **Perhitungan:**
   - Deteksi objek referensi di frame
   - Ukur dimensi piksel dan depth relatif
   - Hitung scale factor:
     ```
     width_real (m) = (width_px × d_rel × S) / fx
     S = (width_real × fx) / (width_px × d_rel)
     ```

**Solusi 3: Multi-Frame Consistency (Jika memungkinkan)**

- Gunakan visual odometry atau IMU untuk estimasi pergerakan
- Triangulasi depth dari beberapa viewpoint
- Fuse dengan GPS/GNSS untuk validasi skala

**C. Ekstraksi Region dan Perhitungan dengan Robust Statistics**

Untuk setiap lubang yang terdeteksi YOLOv8:

1. **Ambil ROI dari Depth Map:**
   - **Prefer:** Gunakan segmentation mask untuk area presisi
   - **Fallback:** Gunakan bounding box dengan margin kecil

2. **Identifikasi Depth Surface (Permukaan Jalan):**
   - Ambil border pixels di sekitar lubang (5-10 pixel band)
   - **Metode Robust:** `Z_surface = median(border_depth)` ← tahan terhadap outlier
   - Bukan mean (rentan terhadap noise)

3. **Identifikasi Depth Base (Dasar Lubang):**
   - Ambil depth values di dalam ROI
   - **Outlier Removal dengan IQR:**
     ```python
     Q1 = np.percentile(roi_depth, 25)
     Q3 = np.percentile(roi_depth, 75)
     IQR = Q3 - Q1
     lower_bound = Q1 - 1.5 × IQR
     upper_bound = Q3 + 1.5 × IQR
     filtered_depth = roi_depth[(roi_depth > lower_bound) & 
                                 (roi_depth < upper_bound)]
     ```
   - **Metode Robust:** `Z_base = percentile(filtered_depth, 10)` ← ambil bagian terdalam

4. **Hitung Diameter (Metrik Real-World):**
   
   **Untuk Bounding Box:**
   ```python
   # Ambil average depth di ROI
   Z_avg = (Z_surface + Z_base) / 2
   
   # Konversi pixel width ke metrik
   diameter_cm = (bbox_width_px × Z_avg × 100) / fx
   ```
   
   **Untuk Segmentation Mask (Lebih Akurat):**
   ```python
   # Fit ellipse pada mask contour
   contour = cv2.findContours(mask, ...)
   ellipse = cv2.fitEllipse(contour)
   (center, axes, angle) = ellipse
   major_axis_px = max(axes)
   
   # Konversi major axis ke metrik
   diameter_cm = (major_axis_px × Z_avg × 100) / fx
   ```

5. **Hitung Kedalaman Lubang:**
   ```python
   depth_cm = (Z_surface - Z_base) × 100  # cm
   ```

**D. Perspective Correction (Opsional untuk Akurasi Tinggi)**

Jika kamera memiliki pitch/roll angle signifikan:

1. **Estimasi Road Plane:**
   - Gunakan RANSAC untuk fit plane pada titik-titik jalan
   - Extract normal vector road plane

2. **Homography Transformation:**
   - Transformasi depth map ke bird's-eye view
   - Ukuran diameter menjadi tidak tergantung pada angle kamera

3. **Alternative: IMU Fusion:**
   - Gunakan IMU data untuk kompensasi orientation
   - Koreksi measurement berdasarkan pitch/roll real-time

**E. Pelacakan Objek Lintas Frame (BoT-SORT)**

- **Tujuan:** Menjaga ID konsisten untuk setiap lubang di beberapa frame
- **Input:** Bounding boxes/masks dari YOLOv8 + feature embeddings
- **Output:** Track ID unik (Pothole_001, Pothole_002, dst.)
- **Feature:** Re-identification untuk handle temporary occlusion
- **Buffer:** Simpan N frame terakhir (10-30) per track ID

**F. Pemfilteran Temporal (Kalman Filter - CDKF)**

- **Tujuan:** Menghaluskan fluktuasi pengukuran antar frame
- **Input:** Rangkaian pengukuran untuk setiap Track ID
  ```
  Track_001: 
    - diameter: [45.2, 47.1, 44.8, 46.3, 45.9, ...]
    - depth: [10.5, 11.2, 10.8, 11.0, 10.7, ...]
  ```

- **State Vector:**
  ```
  x = [diameter, depth, velocity_diameter, velocity_depth]^T
  ```

- **Process:**
  1. **Prediction Step:**
     ```
     x_pred = F × x_prev
     P_pred = F × P × F^T + Q
     ```
     - F: state transition matrix
     - Q: process noise covariance (tuning parameter)

  2. **Update Step:**
     ```
     K = P_pred × H^T × (H × P_pred × H^T + R)^(-1)
     x_updated = x_pred + K × (z - H × x_pred)
     P_updated = (I - K × H) × P_pred
     ```
     - H: observation matrix
     - R: measurement noise covariance (tuning parameter)
     - z: current measurement

- **Tuning Noise Parameters:**
  - **Process Noise Q:** Seberapa cepat state berubah
    - Tinggi: filter lebih responsif, kurang smooth
    - Rendah: filter lebih smooth, kurang responsif
  - **Measurement Noise R:** Seberapa percaya pada measurement
    - Tinggi: kurang percaya measurement, lebih smooth
    - Rendah: lebih percaya measurement, kurang smooth
  - **Eksperimen:** Grid search dengan ground truth validation

- **Output:** Estimasi final setelah track stabil (misal: setelah 10 frames)

#### 3.5.4 Kelebihan Metode dengan Enhancement

1. **Efisiensi Hardware:** Hanya butuh satu kamera (praktis dan murah)
2. **Pengukuran Simultan:** Diameter dan kedalaman dari satu pipeline
3. **Robust terhadap Noise:** Filtering temporal + robust statistics
4. **Scale Absolut:** Scale recovery memberikan ukuran metrik akurat
5. **Tidak Terbatas Asumsi Jalan Datar:** Optional perspective correction
6. **State-of-the-Art:** DepthAnything V2 + best practices engineering
7. **Akurasi Tinggi:** Segmentation mask + outlier removal + Kalman filter

#### 3.5.5 Tantangan dan Mitigasi (Update)

| Tantangan | Strategi Mitigasi | Status |
|-----------|-------------------|--------|
| **Skala absolut depth map** | Height-based scale recovery dengan kalibrasi tinggi kamera | **Teratasi** |
| **Noise pada depth map** | Median + percentile + IQR outlier removal | **Teratasi** |
| **Bbox vs bentuk lubang** | Gunakan instance segmentation (YOLOv8-seg) + ellipse fitting | **Teratasi** |
| **Variasi pencahayaan** | Augmentasi dataset + normalisasi input | Diminimalisir |
| **Oklusi kendaraan lain** | BoT-SORT dengan re-identification features | Diminimalisir |
| **Latensi komputasi** | Optimasi TensorRT/ONNX + YOLOv8n/s | Dalam proses |
| **Kalibrasi berubah** | Prosedur re-kalibrasi cepat + check reprojection error | Terdokumentasi |
| **Error focal length fx** | Kalibrasi presisi + validasi dengan objek ukuran diketahui | **Teratasi** |
| **Jalan miring/kamera miring** | Optional: Homography / IMU fusion | Future work |

### 3.6 Evaluasi dan Validasi

#### 3.6.1 Ground Truth Collection

**Pengukuran Lapangan:**
- Diameter: Gunakan meteran/kaliper untuk ukur lebar maksimum lubang
- Kedalaman: Gunakan depth gauge atau ruler tegak lurus
- Lakukan 3 kali pengukuran per lubang, ambil rata-rata
- Dokumentasi foto dari berbagai angle

**Metadata:**
- ID lubang, lokasi GPS presisi, timestamp
- Kondisi: pencahayaan, cuaca, tipe jalan
- Ground truth pairing dengan frame video

#### 3.6.2 Eksperimen Ablation Study

**Tujuan:** Memahami kontribusi setiap komponen

| Eksperimen | Konfigurasi | Metrik |
|------------|-------------|--------|
| Baseline | Bbox + mean depth | MAE, RMSE |
| + Segmentation | Mask + mean depth | MAE, RMSE |
| + Robust Stats | Mask + median/percentile | MAE, RMSE |
| + Scale Recovery | + Height-based scaling | MAE, RMSE |
| + Tracking | + BoT-SORT | Stability |
| + Kalman (Full) | + Temporal filtering | MAE, RMSE, Stability |

**Variabel Tuning:**
- Percentile untuk Z_base: 5%, 10%, 15%, 20%
- Kalman noise parameters: Q, R grid search
- Temporal window size: 10, 20, 30 frames

#### 3.6.3 Validasi Scale Recovery

**Test dengan Objek Referensi:**
- Letakkan marker dengan ukuran diketahui (misal: 30cm box) pada berbagai jarak
- Bandingkan estimasi vs ground truth
- Hitung % error untuk setiap jarak (1m, 3m, 5m, 10m)

**Test dengan Berbagai Tinggi Kamera:**
- Simulasi mounting height: 1.0m, 1.5m, 2.0m
- Verifikasi konsistensi scale factor

#### 3.6.4 Sensitivitas Parameter Kamera

**Test Robustness terhadap Error Kalibrasi:**
- Simulasi error fx: ±1%, ±3%, ±5%
- Analisis dampak pada diameter dan depth estimation
- Plot error propagation

### 3.7 Desain Arsitektur Sistem dan API

**Alur Kerja:**
```
Kamera → Undistort → YOLOv8 Inference → Extract BBox/Mask 
→ Depth Estimation → Scale Recovery → Compute Diameter & Depth 
→ Tracking → Kalman Filter → Build JSON Payload 
→ REST API POST → Dashboard Update
```

**Implementasi:** Edge device (NVIDIA Jetson Nano/Xavier NX)

**Optimasi Edge Deployment (ONNX/TensorRT):**
- Export model: `yolo export format=onnx` atau `engine` (TensorRT) untuk latensi rendah.
- Pertimbangkan INT8 quantization (perlu kalibrasi representative dataset) untuk throughput lebih tinggi.
- Batasi resolusi input sesuai target FPS dan budget memori.

**API Endpoint:** `POST /api/v1/potholes/report`

**Contoh Payload JSON:**
```json
{
  "id": "pothole_20251001_12345",
  "latitude": -5.14769,
  "longitude": 119.43232,
  "timestamp": "2025-10-01T10:15:30Z",
  "confidence": 0.88,
  "size": {
    "diameter_cm": 52.5,
    "depth_cm": 11.2,
    "measurement_method": "depth_estimation_v2",
    "measurement_confidence": 0.92,
    "frames_tracked": 15
  },
  "severity": "berat",
  "severity_classification": {
    "depth_category": "berat",
    "diameter_category": "besar",
    "priority_score": 8.5
  },
  "measurement_metadata": {
    "scale_recovery_method": "height_based",
    "scale_factor": 1.23,
    "camera_height_m": 1.5,
    "focal_length_px": 800.5,
    "segmentation_used": true,
    "kalman_iterations": 15
  },
  "image_url": "https://storage.cloud/pothole_images/img_12345.jpg",
  "device_id": "dashcam_unit_042"
}
```

### 3.6 Metrik Evaluasi
- Deteksi: mAP@0.5, Precision, Recall, F1, FPS, Latency.  
- Ukuran: MAE, RMSE, % error vs ground truth.  
- Sistem: latensi end-to-end, success rate API, dampak akurasi GPS.

### 3.7 Jadwal Penelitian 
1–3: Literatur & dataset. 4–6: Pelatihan YOLOv8 & augmentasi. 7–9: Estimasi ukuran terintegrasi (DepthAnything + Kalman). 10–11: API & dashboard. 12–14: Integrasi & uji lapangan. 15–16: Analisis & penulisan.

### 3.8 Risiko & Mitigasi 
- Presisi skala depth rendah → kalibrasi tinggi kamera/marker referensi; scale recovery.  
- Artifak cuaca/pencahayaan → augmentasi & normalisasi.  
- Latensi edge → optimisasi (TensorRT/ONNX), pakai YOLO ringan.  
- Tracking loss → BoT-SORT dengan re-id; jendela temporal.  
- Sensitivitas kalibrasi → verifikasi lapangan rutin.

### 3.9 Checklist Praktis Implementasi
- [ ] Kalibrasi kamera (K, dist) dan simpan.  
- [ ] Verifikasi depth absolut/relatif; siapkan scale recovery.  
- [ ] Gunakan segmentasi mask bila memungkinkan.  
- [ ] Pakai median & percentile; hilangkan outlier.  
- [ ] Urutan: undistort → detect → depth.  
- [ ] Catat metadata (H kamera, fx, cx, cy, mounting angle).  
- [ ] Validasi lapangan dengan pengukuran manual.  
- [ ] Tuning Kalman & threshold via validasi.

### 3.10 Aturan Severity (Contoh, dapat disesuaikan)
- Kedalaman (depth):
  - Ringan: < 2.5 cm  
  - Sedang: 2.5 – 7.5 cm  
  - Berat: ≥ 7.5 cm

- Diameter (lebar lubang):
  - Kecil: < 30 cm  
  - Sedang: 30 – 60 cm  
  - Besar: ≥ 60 cm

- Aturan gabungan (prioritas konservatif):
  - Berat jika depth Berat OR diameter Besar
  - Sedang jika depth Sedang OR diameter Sedang (dan bukan Berat)
  - Ringan selain itu

Catatan: Sesuaikan ambang dengan regulasi lokal dan studi lapangan.

### 3.11 Etika, Privasi, dan Tata Kelola Data
- Hindari merekam informasi pribadi (wajah, plat) jika tidak diperlukan; lakukan blur/anonymization saat penyimpanan atau pelaporan publik.
- Simpan data sesuai kebijakan institusi/pemerintah; enkripsi saat transit (HTTPS) dan at-rest bila sensitif.
- Dokumentasikan consent/izin perekaman di area publik sesuai regulasi setempat.

### 3.12 Keterbatasan dan Arah Pekerjaan Lanjutan
- Ketergantungan pada scale recovery membuat akurasi absolut sensitif terhadap H, pitch, dan pemilihan ROI_road.
- Depth monokular tetap rentan pada kondisi pencahayaan ekstrem atau tekstur minim.
- Peningkatan potensial: stereo/struktur-dari-gerak (VO/SLAM), sensor tambahan (IMU/GNSS), segmentasi kelas jalan untuk ROI_road yang lebih andal, dan pengukuran 3D berbasis plane fitting di sekitar lubang.

---

## BAB 4: KONTRIBUSI YANG DIHARAPKAN
1. Prototipe end-to-end deteksi + pelaporan pothole real-time dengan estimasi ukuran terintegrasi.  
2. Metode monokular berbasis DepthAnything V2 dengan stabilisasi temporal untuk diameter & kedalaman.  
3. Prototipe API dan arsitektur siap adopsi untuk pemerintah daerah.

---

## REFERENSI
1. Gorro et al. (2024). JOIG: YOLOv8 + augmentation for pothole detection  
2. Wang et al. (2025). Integrated monocular depth estimation with temporal filtering for robust measurement. arXiv:2505.21049  
3. DepthAnything V2 Documentation. Dense Prediction Transformer for monocular depth estimation  
4. BoT-SORT: Robust Associations Multi-Pedestrian Tracking. arXiv:2206.14651  
5. Hoseini et al. (2024). Deep learning architectures for real-time object detection
