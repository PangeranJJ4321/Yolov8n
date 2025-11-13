# Halaman 1: RMC (Research Management Committee)

**SISTEM INFORMASI CERDAS UNTUK DETEKSI, ESTIMASI UKURAN, DAN PELAPORAN OTOMATIS JALAN BERLUBANG SECARA REAL-TIME MENGGUNAKAN YOLOV8**

---

## RINGKASAN EKSEKUTIF

### Informasi Penelitian

**Peneliti:** Pangeran Juhrifar Jafar  
**NIM:** H071231056  
**Program Studi:** Sistem Informasi  
**Fakultas:** Matematika dan Ilmu Pengetahuan Alam  
**Universitas:** Universitas Hasanuddin  
**Pembimbing:** Pak Supri

---

### Abstrak Penelitian

Indonesia menghadapi tantangan signifikan dalam pemeliharaan infrastruktur jalan dengan **30% dari 496.000 km jalan** dalam kondisi rusak ringan hingga berat. Penelitian ini mengembangkan sistem informasi cerdas terintegrasi untuk **deteksi, estimasi ukuran, dan pelaporan otomatis** jalan berlubang secara real-time menggunakan teknologi YOLOv8 dan depth estimation monokular.

**Kontribusi Utama:**
1. **Deteksi Real-time:** Implementasi YOLOv8 dengan akurasi mAP@0.5 = 0.85
2. **Estimasi Ukuran Simultan:** Pengukuran diameter dan kedalaman menggunakan DepthAnything V2 dengan error < 5%
3. **Sistem Terintegrasi:** REST API untuk pelaporan otomatis ke dashboard pemerintah

**Target Performa:**
- Akurasi Deteksi: mAP@0.5 = 0.85
- Kecepatan: 20 FPS pada RTX 3060
- Akurasi Ukuran: MAE diameter 3.2 cm, MAE kedalaman 1.4 cm
- Latency: < 50ms per frame

---

### Masalah yang Ingin Diselesaikan

**Keterbatasan Metode Konvensional:**
- Laporan manual dan inspeksi lapangan lambat dan tidak efisien
- Kecepatan, akurasi, dan cakupan geografis terbatas
- Proses reaktif, bukan proaktif

**Tantangan Teknis:**
- Pengukuran dimensi kerusakan jalan dari citra monokular
- Tantangan skala absolut pada depth estimation
- Kebutuhan real-time processing dengan latensi rendah

**Gap Implementasi:**
- Implementasi sistem AI untuk infrastruktur jalan di Indonesia masih terbatas
- Belum ada sistem terintegrasi deteksi + pengukuran + pelaporan

---

### Tujuan dan Metode Penelitian

**Tujuan Utama:**
1. Mengimplementasikan sistem deteksi real-time menggunakan YOLOv8
2. Mengembangkan estimasi ukuran terintegrasi dengan DepthAnything V2
3. Mengimplementasikan sistem pelacakan dan filtering temporal
4. Merancang prototipe REST API untuk pelaporan otomatis

**Metodologi:**
- **Jenis Penelitian:** Eksperimental dengan pendekatan kuantitatif
- **Objek Penelitian:** Model YOLOv8n, dataset potholes, sistem depth estimation
- **Teknik Pengumpulan Data:** Dataset Roboflow, kalibrasi kamera, pengujian real-time
- **Teknik Analisis:** Metrik mAP, precision, recall, FPS, MAE

---

### Teknologi dan Inovasi

**Stack Teknologi:**
- **Deep Learning:** YOLOv8 (CSPDarknet53 backbone)
- **Depth Estimation:** DepthAnything V2 (DPT architecture)
- **Tracking:** BoT-SORT dengan re-identification
- **Filtering:** Kalman Filter untuk temporal smoothing
- **API:** REST API dengan format JSON
- **Statistics:** Robust statistics (median, percentile, IQR)

**Keunggulan Sistem:**
- ✅ **End-to-End Pipeline:** Deteksi → Estimasi Ukuran → Pelaporan
- ✅ **Real-time Processing:** Latensi < 50ms dengan throughput 20 FPS
- ✅ **Akurasi Tinggi:** Error estimasi ukuran < 5%
- ✅ **Scalable Architecture:** Dapat diimplementasikan di berbagai kota

---

### Manfaat dan Dampak

**Bagi Pemerintah:**
- Alat bantu pengambilan keputusan berbasis data real-time
- Pemeliharaan jalan lebih efisien dan proaktif
- Pengukuran terukur dan objektif

**Bagi Masyarakat:**
- Meningkatkan keselamatan berkendara
- Mempercepat proses identifikasi dan perbaikan jalan rusak
- Kenyamanan berkendara yang lebih baik

**Bagi Akademisi:**
- Kontribusi prototipe sistem end-to-end
- Analisis mendalam tantangan depth estimation monokular
- Best practices untuk aplikasi real-world

---

### Timeline dan Sumber Daya

**Timeline Penelitian:** 16 Minggu

**Minggu 1-3:** Literatur & Dataset  
**Minggu 4-6:** Pelatihan YOLOv8  
**Minggu 7-9:** Estimasi Ukuran Terintegrasi  
**Minggu 10-11:** API & Dashboard  
**Minggu 12-14:** Integrasi & Uji Lapangan  
**Minggu 15-16:** Analisis & Penulisan

**Sumber Daya:**
- **Hardware:** GPU RTX 3060, CPU i7-12700K, 32GB RAM
- **Software:** PyTorch, OpenCV, Ultralytics YOLOv8, DepthAnything V2
- **Dataset:** Roboflow Potholes Dataset, RDD2022

---

### Kontribusi yang Diharapkan

**Kontribusi Teoritis:**
- Metodologi depth estimation monokular untuk aplikasi infrastruktur jalan
- Framework terintegrasi computer vision + deep learning + sistem informasi
- Solusi scale recovery dalam depth estimation monokular

**Kontribusi Praktis:**
- Prototipe sistem end-to-end siap implementasi
- REST API terintegrasi dengan format data komprehensif
- Dokumentasi lengkap untuk implementasi real-world

**Kontribusi Sosial:**
- Meningkatkan keselamatan berkendara
- Mendukung program smart city
- Pengurangan biaya pemeliharaan infrastruktur

---

### Status Risiko dan Mitigasi

| Risiko | Probabilitas | Dampak | Mitigasi | Status |
|--------|--------------|--------|----------|--------|
| Akurasi depth estimation rendah | Medium | High | Kalibrasi kamera presisi, validasi ground truth | Teratasi |
| Scale recovery tidak akurat | Medium | High | Multiple reference objects | Teratasi |
| Latensi sistem tinggi | High | Medium | Optimasi model, YOLOv8n | Dalam proses |
| Tracking loss pada occlusion | Medium | Medium | BoT-SORT dengan re-ID | Teratasi |
| Dataset tidak representatif | Low | High | Data augmentation, multiple sources | Teratasi |

---

**Tanggal Penyusunan:** [Tanggal]  
**Status:** Proposal Penelitian

---

\pagebreak

# Halaman 2: BAB I - PENDAHULUAN

---

## BAB I - PENDAHULUAN

### 1.1 Latar Belakang

Infrastruktur jalan merupakan fondasi fundamental bagi pembangunan ekonomi dan sosial suatu negara. Jalan yang berkualitas baik tidak hanya memfasilitasi mobilitas masyarakat, tetapi juga mendukung pertumbuhan ekonomi, aksesibilitas layanan publik, dan konektivitas antarwilayah. Dalam konteks pembangunan berkelanjutan, infrastruktur jalan yang memadai menjadi indikator penting kemajuan suatu bangsa dan kesejahteraan masyarakatnya.

Indonesia sebagai negara kepulauan dengan geografi yang kompleks menghadapi tantangan besar dalam pemeliharaan infrastruktur jalan. Data Kementerian Pekerjaan Umum dan Perumahan Rakyat menunjukkan bahwa dari total 496.000 km jalan di Indonesia, sekitar 30% berada dalam kondisi rusak ringan hingga berat. Masalah jalan berlubang (*potholes*) menjadi fenomena yang sangat umum, terutama di daerah dengan curah hujan tinggi dan beban lalu lintas yang berat. Kondisi ini tidak hanya mengganggu kenyamanan berkendara, tetapi juga menimbulkan risiko keselamatan yang serius dan kerugian ekonomi yang signifikan.

Perkembangan teknologi informasi dan komunikasi telah membuka peluang baru dalam mengatasi permasalahan infrastruktur jalan. Teknologi *Computer Vision* dan *Artificial Intelligence* (AI) menawarkan solusi inovatif untuk deteksi otomatis kerusakan jalan secara real-time. Kemajuan dalam bidang *Deep Learning*, khususnya *Convolutional Neural Networks* (CNN), telah merevolusi kemampuan sistem untuk mengenali dan menganalisis kondisi jalan secara akurat dan efisien.

Beberapa negara maju telah mengimplementasikan sistem deteksi kerusakan jalan berbasis AI dengan hasil yang menggembirakan. Singapura menggunakan sistem *Smart Nation* yang mengintegrasikan sensor dan kamera untuk monitoring infrastruktur secara real-time. Jepang mengembangkan sistem *Road Damage Detection* menggunakan *Machine Learning* untuk mengidentifikasi berbagai jenis kerusakan jalan. Di Indonesia, beberapa kota besar seperti Jakarta dan Surabaya telah mulai mengadopsi teknologi *smart city*, namun implementasi sistem deteksi kerusakan jalan yang komprehensif masih terbatas dan belum terintegrasi dengan baik.

Metode konvensional deteksi kerusakan jalan di Indonesia masih mengandalkan laporan manual dari masyarakat dan inspeksi lapangan oleh petugas, yang memiliki keterbatasan dalam hal kecepatan, akurasi, dan cakupan. Proses ini bersifat reaktif, subjektif, dan seringkali tidak tepat waktu. Terdapat gap yang signifikan antara kebutuhan pemeliharaan jalan yang proaktif dengan kemampuan deteksi yang tersedia. Peluang besar terbuka untuk mengembangkan sistem otomatis yang dapat mendeteksi, mengukur, dan melaporkan kerusakan jalan secara real-time dengan akurasi tinggi.

Sistem informasi memainkan peran krusial dalam mengintegrasikan teknologi deteksi kerusakan jalan dengan proses pengambilan keputusan yang efektif. Melalui *Application Programming Interface* (API) dan *dashboard* interaktif, data hasil deteksi dapat diolah, dianalisis, dan disajikan kepada stakeholder dalam format yang mudah dipahami. Sistem informasi yang terintegrasi memungkinkan otomasi proses pelaporan, prioritisasi perbaikan, dan monitoring progress secara real-time, sehingga mentransformasi manajemen infrastruktur jalan dari pendekatan reaktif menjadi proaktif.

Penelitian sebelumnya telah menunjukkan potensi besar teknologi *Deep Learning* dalam deteksi kerusakan jalan. Gorro et al. (2024) berhasil mengimplementasikan YOLOv8 dengan augmentasi data untuk deteksi lubang jalan dengan akurasi tinggi. Wang et al. (2025) mengembangkan sistem terintegrasi yang menggabungkan estimasi kedalaman monokular dengan *temporal filtering* untuk pengukuran ukuran kerusakan yang akurat. Hoseini et al. (2024) mendemonstrasikan efektivitas arsitektur *deep learning* untuk deteksi objek real-time pada kendaraan otonom. Penelitian-penelitian ini memberikan fondasi teoretis yang kuat untuk pengembangan sistem yang lebih komprehensif.

Berdasarkan analisis gap dan peluang yang ada, penelitian ini bertujuan untuk mengembangkan sistem informasi cerdas yang mengintegrasikan teknologi YOLOv8 untuk deteksi jalan berlubang secara real-time, estimasi ukuran kerusakan menggunakan *depth estimation* monokular, dan sistem pelaporan otomatis melalui REST API. Sistem ini diharapkan dapat mengatasi keterbatasan metode konvensional dengan menyediakan solusi yang akurat, efisien, dan dapat diimplementasikan secara praktis untuk mendukung program *smart city* dan pembangunan infrastruktur berkelanjutan di Indonesia.

### 1.2 Identifikasi Masalah

Berdasarkan analisis latar belakang yang telah diuraikan, dapat diidentifikasi beberapa permasalahan mendasar yang menjadi fokus penelitian ini:

**Permasalahan Utama:**

1. **Keterbatasan Metode Konvensional:** Sistem deteksi kerusakan jalan yang ada saat ini masih mengandalkan laporan manual dan inspeksi lapangan, yang memiliki keterbatasan dalam hal kecepatan, akurasi, dan cakupan geografis.

2. **Tantangan Teknis Depth Estimation:** Pengukuran dimensi kerusakan jalan (diameter dan kedalaman) dari citra monokular menghadapi tantangan skala absolut, di mana model deep learning umumnya hanya menghasilkan estimasi kedalaman relatif.

3. **Integrasi Sistem yang Terfragmentasi:** Belum ada sistem terintegrasi yang dapat menggabungkan deteksi, pengukuran, dan pelaporan kerusakan jalan dalam satu platform yang efisien dan dapat diakses oleh berbagai stakeholder.

4. **Kebutuhan Real-time Processing:** Aplikasi praktis memerlukan sistem yang dapat beroperasi secara real-time dengan latensi rendah, terutama untuk implementasi pada kendaraan yang bergerak.

5. **Gap Implementasi di Indonesia:** Meskipun teknologi sudah tersedia, implementasi sistem deteksi kerusakan jalan berbasis AI di Indonesia masih terbatas dan belum terintegrasi dengan sistem manajemen infrastruktur yang ada.

### 1.3 Rumusan Masalah

Berdasarkan identifikasi masalah yang telah diuraikan, rumusan masalah dalam penelitian ini adalah:

1. Bagaimana merancang dan mengimplementasikan model **YOLOv8** untuk dapat mendeteksi jalan berlubang secara akurat dan *real-time* dari input video kamera dalam berbagai kondisi jalan?

2. Bagaimana mengembangkan metode untuk mengestimasi **diameter (2D)** dan **kedalaman (3D)** lubang secara akurat dan simultan dari citra kamera monokular dengan mengatasi tantangan skala absolut pada depth estimation?

3. Bagaimana merancang arsitektur sistem yang dapat mengirimkan data hasil deteksi (koordinat GPS, ukuran, *timestamp*) secara otomatis melalui **REST API** ke sebuah *dashboard* pemantauan?

### 1.4 Tujuan Penelitian

Tujuan dari penelitian ini adalah:

1. Mengimplementasikan sistem deteksi jalan berlubang secara *real-time* menggunakan model YOLOv8 (varian ringan seperti YOLOv8n atau YOLOv8s untuk latensi rendah).

2. Mengembangkan metode terintegrasi untuk mengestimasi **diameter** dan **kedalaman** lubang secara simultan menggunakan estimasi kedalaman monokular berbasis deep learning (DepthAnything V2) dengan penerapan **scale recovery** untuk akurasi metrik absolut.

3. Mengimplementasikan sistem pelacakan objek (BoT-SORT) dan pemfilteran temporal (Kalman Filter) untuk meningkatkan stabilitas dan akurasi pengukuran.

4. Menerapkan teknik **robust statistics** (median, percentile, outlier removal) untuk mengatasi noise pada depth map.

5. Merancang dan membuat prototipe **REST API** untuk mengirimkan data hasil deteksi ke sebuah *dashboard* simulasi pihak berwenang.

### 1.5 Manfaat Penelitian

Penelitian ini diharapkan memberikan manfaat:

1. **Bagi Pemerintah/Otoritas Jalan:** Menyediakan alat bantu pengambilan keputusan yang berbasis data *real-time* untuk pemeliharaan jalan yang lebih efisien, proaktif, dan terukur dengan klasifikasi severity otomatis.

2. **Bagi Masyarakat:** Meningkatkan keselamatan dan kenyamanan berkendara dengan mempercepat proses identifikasi dan perbaikan jalan yang rusak.

3. **Bagi Akademisi:** Memberikan kontribusi berupa prototipe sistem *end-to-end* dengan analisis mendalam tentang tantangan implementasi depth estimation monokular, solusi scale recovery, dan best practices untuk aplikasi real-world.

### 1.6 Signifikansi Penelitian

Penelitian ini memiliki signifikansi yang tinggi dalam beberapa aspek:

**Signifikansi Teoritis:**
- Memberikan kontribusi dalam pengembangan metodologi depth estimation monokular untuk aplikasi infrastruktur jalan
- Mengembangkan framework terintegrasi yang menggabungkan computer vision, deep learning, dan sistem informasi
- Menyediakan solusi untuk tantangan scale recovery dalam depth estimation monokular

**Signifikansi Praktis:**
- Menyediakan solusi teknologi yang dapat diimplementasikan secara langsung oleh otoritas jalan
- Mengurangi biaya operasional dan meningkatkan efisiensi pemeliharaan infrastruktur
- Meningkatkan kualitas layanan publik melalui sistem monitoring yang lebih baik

**Signifikansi Sosial:**
- Meningkatkan keselamatan berkendara dan mengurangi risiko kecelakaan
- Meningkatkan kualitas hidup masyarakat melalui infrastruktur jalan yang lebih baik
- Mendukung program smart city dan pembangunan berkelanjutan

**Signifikansi Ekonomi:**
- Mengurangi biaya perawatan kendaraan akibat kerusakan jalan
- Meningkatkan efisiensi logistik dan transportasi
- Menciptakan peluang bisnis baru dalam bidang teknologi infrastruktur

### 1.7 Batasan Masalah

Penelitian ini dibatasi pada:

1. **Model yang Digunakan:** Hanya menggunakan YOLOv8n (nano version) untuk deteksi objek
2. **Jenis Kerusakan:** Fokus pada deteksi lubang jalan (potholes) saja, tidak termasuk jenis kerusakan jalan lainnya
3. **Kondisi Lingkungan:** Evaluasi dilakukan pada kondisi normal (siang hari, cuaca cerah)
4. **Platform Implementasi:** Sistem diimplementasikan pada platform desktop/laptop
5. **Area Geografis:** Testing dilakukan di area terbatas dengan karakteristik jalan yang spesifik
6. **Kamera:** Menggunakan kamera monokular standar, bukan kamera stereo atau multi-view
7. **Dataset:** Menggunakan dataset yang tersedia secara publik dengan anotasi terbatas

### 1.8 Landasan Teori

Landasan teori dalam penelitian ini mencakup konsep-konsep fundamental yang menjadi dasar pengembangan sistem deteksi, estimasi ukuran, dan pelaporan otomatis jalan berlubang. Teori-teori ini meliputi:

**1. Computer Vision dan Deep Learning:**
Computer vision adalah bidang ilmu yang mempelajari bagaimana komputer dapat menafsirkan dan memahami informasi visual dari dunia nyata (Albawi et al., 2017). Bidang ini mencakup pengembangan algoritma dan sistem yang memungkinkan mesin untuk mengekstrak, menganalisis, dan memahami informasi bermakna dari gambar atau video digital. Computer vision memiliki aplikasi luas dalam berbagai domain seperti pengenalan objek, segmentasi citra, deteksi gerakan, dan analisis medis.

Deep learning, khususnya Convolutional Neural Networks (CNN), telah merevolusi computer vision dengan kemampuannya mempelajari fitur-fitur kompleks secara otomatis dari data mentah (LeCun et al., 2015). CNN meniru cara kerja sistem visual manusia dengan menggunakan lapisan-lapisan konvolusi yang dapat mendeteksi pola lokal seperti tepi, tekstur, dan bentuk. Arsitektur ini memungkinkan model untuk mempelajari representasi hierarkis dari fitur low-level hingga high-level secara end-to-end, mengatasi keterbatasan metode tradisional yang mengandalkan hand-crafted features.

**2. Object Detection:**
Object detection adalah teknik computer vision yang dapat melokalisasi dan mengklasifikasi objek dalam citra secara simultan (Zhao et al., 2019). Berbeda dengan klasifikasi yang hanya mengidentifikasi objek dalam gambar, object detection memberikan informasi spasial yang tepat tentang lokasi objek melalui bounding box. Teknik ini melibatkan dua tugas utama: (1) lokalisasi objek dengan prediksi koordinat bounding box, dan (2) klasifikasi objek dengan prediksi class label.

YOLO (You Only Look Once) merupakan salah satu algoritma object detection yang terkenal karena kecepatan dan akurasinya dalam aplikasi real-time (Redmon et al., 2016). YOLO memperkenalkan pendekatan revolusioner dengan memproses seluruh citra dalam satu kali forward pass, berbeda dengan metode two-stage yang memerlukan proposal generation terlebih dahulu. Arsitektur YOLO menggunakan grid-based approach dimana setiap grid cell bertanggung jawab untuk mendeteksi objek yang center-nya berada di dalam cell tersebut.

**3. Monocular Depth Estimation:**
Monocular depth estimation adalah teknik untuk memperkirakan kedalaman objek dari citra tunggal tanpa menggunakan kamera stereo (Eigen & Fergus, 2015). Teknik ini mengatasi keterbatasan kamera stereo yang memerlukan dua kamera yang terkalibrasi dengan baik dan memiliki baseline yang cukup. Monocular depth estimation sangat berguna untuk aplikasi mobile dan embedded systems dimana space dan power constraints menjadi pertimbangan penting.

Teknik ini menggunakan model deep learning untuk menghasilkan depth map yang menunjukkan jarak relatif setiap piksel dari kamera (Godard et al., 2017). Model dilatih menggunakan dataset yang berisi pasangan citra RGB dan ground truth depth map. Selama training, model mempelajari mapping dari fitur visual (warna, tekstur, perspektif) ke informasi kedalaman. Namun, estimasi kedalaman monokular hanya menghasilkan depth relatif, sehingga diperlukan scale recovery untuk konversi ke satuan metrik absolut.

**4. Scale Recovery:**
Scale recovery adalah proses konversi estimasi kedalaman relatif menjadi kedalaman absolut dalam satuan metrik (Laina et al., 2016). Proses ini merupakan tantangan utama dalam monocular depth estimation karena model hanya dapat memprediksi depth relatif tanpa informasi skala absolut. Scale recovery memerlukan referensi ukuran yang diketahui, seperti tinggi mounting kamera atau objek dengan dimensi standar (Ranftl et al., 2021).

Beberapa pendekatan scale recovery yang umum digunakan meliputi: (1) Height-based scale recovery menggunakan tinggi kamera dari permukaan tanah, (2) Object-based scale recovery menggunakan objek dengan ukuran standar seperti manusia atau kendaraan, (3) Multi-frame consistency dengan asumsi gerakan kamera yang smooth, dan (4) Sensor fusion dengan data dari IMU atau GPS. Dalam konteks deteksi potholes, scale recovery memungkinkan konversi pixel dimensions menjadi ukuran fisik yang akurat dalam satuan centimeter atau meter.

**5. Object Tracking:**
Object tracking adalah proses melacak objek yang sama di beberapa frame video secara berurutan (Bewley et al., 2016). Proses ini melibatkan assignment ID yang konsisten untuk objek yang sama sepanjang sequence video, mengatasi masalah occlusion, illumination changes, dan pose variations. Object tracking sangat penting untuk aplikasi real-time karena memungkinkan temporal consistency dan mengurangi false positive deteksi.

BoT-SORT (ByteTrack + ReID) adalah algoritma tracking yang menggabungkan motion prediction dengan appearance features untuk tracking yang robust (Aharon et al., 2022). Algoritma ini menggunakan ByteTrack sebagai base tracker yang mengandalkan motion prediction, kemudian menambahkan re-identification features untuk mengatasi temporary occlusion. BoT-SORT mampu menangani complex scenarios seperti multiple object tracking, occlusion handling, dan identity preservation across frames.

**6. Temporal Filtering:**
Temporal filtering menggunakan informasi dari frame-frame sebelumnya untuk menghasilkan estimasi yang lebih stabil (Kalman, 1960). Teknik ini memanfaatkan temporal correlation dalam video sequence untuk menghaluskan noise dan meningkatkan akurasi estimasi. Temporal filtering sangat penting untuk aplikasi real-time karena dapat mengurangi jitter dan menghasilkan output yang lebih smooth.

Kalman Filter adalah salah satu teknik temporal filtering yang populer untuk menghaluskan noise pada pengukuran berurutan (Welch & Bishop, 2006). Filter ini menggunakan model state space untuk memprediksi state objek (posisi, kecepatan) berdasarkan pengukuran sebelumnya, kemudian mengkoreksi prediksi dengan pengukuran baru. Kalman Filter optimal untuk sistem linear dengan Gaussian noise, dan dapat diadaptasi untuk sistem non-linear menggunakan Extended Kalman Filter atau Unscented Kalman Filter.

**7. REST API:**
REST API (Representational State Transfer Application Programming Interface) adalah arsitektur web service yang menggunakan HTTP protocol untuk komunikasi antar sistem (Fielding, 2000). REST mengikuti prinsip-prinsip stateless, cacheable, dan uniform interface yang membuatnya scalable dan mudah diimplementasikan. API ini memungkinkan pertukaran data dalam format JSON secara efisien dan scalable (Richardson & Ruby, 2007).

REST API menggunakan HTTP methods (GET, POST, PUT, DELETE) untuk operasi CRUD (Create, Read, Update, Delete) pada resources. Setiap resource memiliki unique URI dan dapat direpresentasikan dalam berbagai format seperti JSON, XML, atau HTML. REST API sangat cocok untuk aplikasi web dan mobile karena menggunakan standard HTTP protocol yang didukung oleh semua platform modern.

**8. Real-time Processing:**
Real-time processing adalah kemampuan sistem untuk memproses data input dan menghasilkan output dengan latensi rendah (biasanya < 100ms) (Liu & Layland, 1973). Sistem real-time harus memenuhi deadline constraints untuk memastikan respons yang tepat waktu. Kemampuan ini penting untuk aplikasi interaktif dan sistem yang memerlukan respons cepat (Kopetz, 2011).

Dalam konteks computer vision, real-time processing melibatkan optimasi algoritma untuk mencapai throughput yang tinggi dengan latensi yang rendah. Teknik optimasi meliputi model compression, quantization, pruning, dan hardware acceleration menggunakan GPU atau specialized chips. Real-time processing juga memerlukan efficient data structures dan algorithms yang dapat memproses data streaming dengan minimal buffering.

**9. Robust Statistics:**
Robust statistics adalah teknik statistik yang tahan terhadap outlier dan noise (Huber, 1981). Teknik ini menggunakan estimators yang tidak mudah terpengaruh oleh data yang tidak normal atau mengandung error. Robust statistics sangat penting untuk aplikasi real-world dimana data sering mengandung noise, missing values, atau outliers.

Teknik seperti median, percentile, dan IQR (Interquartile Range) method digunakan untuk menghasilkan estimasi yang lebih stabil (Rousseeuw & Leroy, 2003). Median lebih robust daripada mean karena tidak terpengaruh oleh extreme values. Percentile methods seperti 25th dan 75th percentile dapat digunakan untuk outlier detection. IQR method menggunakan interquartile range untuk mengidentifikasi dan menghilangkan outliers secara otomatis.

**10. Edge Computing:**
Edge computing adalah paradigma komputasi yang memproses data di dekat sumber data, mengurangi latensi dan bandwidth yang diperlukan untuk komunikasi dengan cloud (Shi et al., 2016). Paradigma ini penting untuk aplikasi real-time pada perangkat dengan sumber daya terbatas (Satyanarayanan, 2017). Edge computing memungkinkan processing lokal tanpa mengirim data ke cloud, sehingga mengurangi latency dan meningkatkan privacy.

Dalam konteks computer vision, edge computing memerlukan model yang dioptimasi untuk hardware dengan resources terbatas seperti mobile devices, embedded systems, atau IoT devices. Teknik optimasi meliputi model quantization, pruning, knowledge distillation, dan efficient architectures seperti MobileNet atau EfficientNet. Edge computing juga memerlukan efficient data processing pipelines yang dapat berjalan pada CPU atau specialized AI chips.

---

**Disusun oleh:** Pangeran Juhrifar Jafar  
**NIM:** H071231056  
**Program Studi:** Sistem Informasi  
**Fakultas:** Matematika dan Ilmu Pengetahuan Alam  
**Universitas:** Universitas Hasanuddin

