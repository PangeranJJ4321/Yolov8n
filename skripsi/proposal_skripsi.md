# SKRIPSI

**SISTEM INFORMASI CERDAS UNTUK DETEKSI, ESTIMASI UKURAN, DAN PELAPORAN OTOMATIS JALAN BERLUBANG SECARA REAL-TIME MENGGUNAKAN YOLOV8**

**Disusun oleh:**  
Pangeran Juhrifar Jafar  
NIM: H071231056

**Program Studi:** Sistem Informasi  
**Fakultas:** Matematika dan Ilmu Pengetahuan Alam  
**Universitas:** Universitas Hasabuddin

**Pembimbing:** Pak Supri

---

## DAFTAR ISI

**BAB I - PENDAHULUAN**
- 1.1 Latar Belakang
- 1.2 Identifikasi Masalah
- 1.3 Rumusan Masalah
- 1.4 Tujuan Penelitian
- 1.5 Manfaat Penelitian
- 1.6 Signifikansi Penelitian
- 1.7 Batasan Masalah
- 1.8 Landasan Teori

**BAB II - METODE PENELITIAN**
- 2.1 Jenis Penelitian
- 2.2 Objek Penelitian
- 2.3 Teknik Pengumpulan Data
- 2.4 Teknik Analisis Data
- 2.5 Metodologi Deteksi Kerusakan Jalan
- 2.6 Metodologi Deep Learning untuk Deteksi Kerusakan Jalan
- 2.7 Metodologi Object Detection untuk Deteksi Kerusakan Jalan
- 2.8 Tantangan dalam Deteksi Potholes
- 2.9 Estimasi Ukuran dari Citra Menggunakan Deep Learning Monokular
- 2.10 Arsitektur Sistem Real-time
- 2.11 YOLO (You Only Look Once)
- 2.12 Object Tracking dan Temporal Filtering
- 2.13 REST API dan Sistem Pelaporan

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

## BAB II - METODE PENELITIAN

### 2.1 Jenis Penelitian

Penelitian ini menggunakan metode penelitian **eksperimental** dengan pendekatan **quantitative**. Penelitian eksperimental dipilih karena bertujuan untuk menguji efektivitas model YOLOv8 dalam mendeteksi lubang di jalan melalui eksperimen yang terkontrol.

**Desain Penelitian:**
- **Pre-experimental design** dengan one-group pretest-posttest design
- **Comparative study** untuk membandingkan performa YOLOv8 dengan model lain

### 2.2 Objek Penelitian

**Objek Penelitian:**
- Model YOLOv8n (You Only Look Once version 8 nano)
- Dataset gambar lubang di jalan (potholes dataset)
- Video real-time untuk testing

**Variabel Penelitian:**

*Variabel Bebas (Independent Variable):*
- Model YOLOv8n
- Parameter training (epochs, batch size, learning rate)
- Preprocessing data

*Variabel Terikat (Dependent Variable):*
- Akurasi deteksi (mAP - mean Average Precision)
- Kecepatan inferensi (FPS - Frames Per Second)
- Precision dan Recall

*Variabel Kontrol:**
- Hardware yang digunakan
- Format input data
- Threshold confidence

### 2.3 Teknik Pengumpulan Data

**1. Dataset Collection:**
- Menggunakan dataset potholes yang tersedia secara publik
- Dataset dibagi menjadi: training (70%), validation (20%), testing (10%)
- Data augmentation untuk meningkatkan variasi data

**2. Data Preprocessing:**
- Resize gambar ke ukuran standar (640x640)
- Normalisasi pixel values
- Label format conversion (YOLO format)

**3. Model Training:**
- Transfer learning dari pre-trained YOLOv8n weights
- Fine-tuning pada dataset potholes
- Hyperparameter tuning

**4. Evaluation Data:**
- Test set untuk evaluasi final
- Video real-time untuk testing performa
- Benchmark dengan model lain

### 2.4 Teknik Analisis Data

**1. Metrik Evaluasi:**
- **mAP (mean Average Precision)**: Akurasi keseluruhan model
- **Precision**: Proporsi deteksi yang benar
- **Recall**: Proporsi objek yang berhasil dideteksi
- **F1-Score**: Harmonic mean dari precision dan recall
- **FPS (Frames Per Second)**: Kecepatan inferensi

**2. Analisis Statistik:**
- Descriptive statistics untuk performa model
- Confusion matrix untuk analisis deteksi
- ROC curve untuk analisis threshold

**3. Visualisasi:**
- Training loss dan validation loss curves
- Detection results visualization
- Performance comparison charts


### 2.5 Metodologi Deteksi Kerusakan Jalan

Deteksi kerusakan jalan merupakan proses identifikasi dan lokalisasi berbagai jenis kerusakan pada permukaan jalan menggunakan teknik computer vision dan machine learning. Metodologi deteksi kerusakan jalan dapat dikategorikan menjadi beberapa pendekatan berdasarkan kompleksitas dan akurasi yang dihasilkan.

**Metode Berbasis Fitur Tradisional:**
Metode ini mengandalkan ekstraksi fitur hand-crafted yang dirancang secara manual untuk mengidentifikasi karakteristik visual kerusakan jalan:

- **Analisis Tekstur:** 
  - Local Binary Pattern (LBP): Mengidentifikasi pola tekstur lokal dengan membandingkan intensitas piksel dengan tetangganya menggunakan operator biner
  - Gray-Level Co-occurrence Matrix (GLCM): Menganalisis distribusi spasial intensitas piksel untuk mengidentifikasi tekstur kasar/halus dengan menghitung probabilitas co-occurrence
  - Gabor Filters: Menggunakan filter bank untuk mendeteksi orientasi dan frekuensi tekstur dengan kernel sinusoidal yang dimodulasi Gaussian

- **Analisis Bentuk:**
  - Canny Edge Detection: Mengidentifikasi tepi objek dengan deteksi gradient yang kuat menggunakan Gaussian smoothing dan non-maximum suppression
  - Sobel Operators: Menggunakan kernel konvolusi untuk mendeteksi perubahan intensitas dalam arah horizontal dan vertikal
  - Laplacian Edge Detection: Menggunakan turunan kedua untuk deteksi tepi yang lebih sensitif terhadap noise
  - Hough Transform: Mendeteksi garis dan bentuk geometris dalam citra menggunakan transformasi parameter space

- **Analisis Warna:**
  - HSV Color Space Segmentation: Memisahkan area kerusakan berdasarkan hue, saturation, dan value untuk mengatasi variasi pencahayaan
  - RGB Thresholding: Menggunakan threshold pada channel warna merah, hijau, dan biru untuk segmentasi sederhana
  - Color Histogram Analysis: Menganalisis distribusi warna untuk mengidentifikasi area abnormal dengan statistik histogram

*[Gambar 2.1: Metodologi deteksi kerusakan jalan berbasis fitur tradisional]*

**Keterbatasan Metode Berbasis Fitur:**
Meskipun metode berbasis fitur menunjukkan kemajuan dibandingkan inspeksi manual, namun memiliki keterbatasan signifikan:

- **Sensitivitas Lingkungan:** Sangat sensitif terhadap variasi pencahayaan (siang/malam), cuaca (hujan/cerah), dan kondisi atmosfer
- **Parameter Tuning:** Memerlukan tuning parameter yang manual dan spesifik untuk setiap kondisi, memakan waktu dan tidak praktis
- **Akurasi Terbatas:** Akurasi rendah (60-70%) pada kondisi real-world yang kompleks dengan variasi yang tinggi
- **Generalization Poor:** Tidak dapat menangani variasi bentuk, ukuran, dan jenis kerusakan yang berbeda
- **Computational Overhead:** Memerlukan multiple feature extraction yang computationally expensive
- **False Positive Rate Tinggi:** Sering mendeteksi bayangan, noda, atau tekstur normal sebagai kerusakan

#### 2.5.1 Metodologi Deep Learning untuk Deteksi Kerusakan Jalan

*Deep Learning* dan *Convolutional Neural Networks* (CNN) telah merevolusi pendekatan deteksi kerusakan jalan dengan kemampuan untuk mempelajari representasi fitur secara otomatis dari data mentah. CNN memiliki kemampuan untuk mempelajari fitur-fitur kompleks secara hierarkis dan adaptif, mengatasi keterbatasan metode tradisional yang mengandalkan hand-crafted features.

**Arsitektur CNN untuk Computer Vision:**

**1. LeNet:** Arsitektur CNN dasar untuk digit recognition
- 7 layers dengan 60,000 parameters
- Convolutional layers + fully connected layers
- Aplikasi: OCR dan digit recognition
- Keterbatasan: Terlalu kecil untuk dataset besar

**2. AlexNet:** Breakthrough dalam ImageNet classification
- 8 layers dengan 60M parameters
- Input: 224x224x3 RGB images
- Architecture: Conv-Conv-Pool-Conv-Conv-Pool-Conv-Conv-Conv-FC-FC-FC
- Innovation: ReLU, Dropout, Local Response Normalization
- Performance: 15.3% top-5 error pada ImageNet

**3. VGG:** Arsitektur yang lebih dalam dengan 16-19 layer
- VGG-16: 16 layers dengan 138M parameters
- VGG-19: 19 layers dengan 144M parameters
- Innovation: Small 3x3 filters, deeper networks
- Performance: 7.3% top-5 error pada ImageNet
- Impact: Menunjukkan bahwa depth adalah kunci performa

**4. ResNet:** Residual connections untuk training deep networks
- ResNet-50: 50 layers dengan 25M parameters
- ResNet-152: 152 layers dengan 60M parameters
- Innovation: Skip connections, batch normalization
- Performance: 3.57% top-5 error pada ImageNet
- Impact: Memungkinkan training networks yang sangat dalam (100+ layers)

**5. EfficientNet:** Optimasi compound scaling
- EfficientNet-B0 hingga B7 dengan scaling yang sistematis
- Innovation: Compound scaling (depth, width, resolution)
- Performance: SOTA efficiency dengan akurasi tinggi
- Impact: Balance optimal antara accuracy dan efficiency

**Keunggulan CNN dalam Deteksi Kerusakan Jalan:**
CNN telah merevolusi deteksi kerusakan jalan dengan kemampuan:
- **Automatic Feature Learning:** Mempelajari fitur yang relevan secara otomatis tanpa intervensi manual
- **Hierarchical Representation:** Fitur low-level (edges, textures) hingga high-level (shapes, objects)
- **Robustness:** Tahan terhadap variasi pencahayaan, cuaca, dan kondisi jalan
- **Scalability:** Dapat dilatih pada dataset besar dengan performa yang konsisten
- **End-to-End Learning:** Dari input image langsung ke output detection tanpa preprocessing manual

**Komponen Utama CNN:**
- **Convolutional Layers:** Ekstraksi fitur lokal menggunakan filter yang dapat dipelajari
- **Pooling Layers:** Reduksi dimensi dan peningkatan invarian terhadap translasi
- **Activation Functions:** ReLU, Leaky ReLU, atau Swish untuk non-linearitas
- **Batch Normalization:** Stabilisasi training dan percepatan konvergensi
- **Dropout:** Regularization untuk mencegah overfitting

*[Gambar 2.2: Arsitektur CNN untuk deteksi kerusakan jalan]*

#### 2.5.2 Metodologi Object Detection untuk Deteksi Kerusakan Jalan

Object detection merupakan metodologi yang merevolusi pendekatan deteksi kerusakan jalan dengan kemampuan untuk melokalisasi dan mengklasifikasi objek secara simultan dalam satu forward pass. Berbeda dengan klasifikasi yang hanya mengidentifikasi objek dalam gambar, object detection dapat memberikan informasi spasial yang tepat tentang lokasi kerusakan jalan.

**Kategori Metodologi Object Detection:**

**1. Two-Stage Detectors:**
- **R-CNN:** Region-based CNN dengan selective search untuk proposal generation
- **Fast R-CNN:** Shared computation untuk multiple regions dengan ROI pooling
- **Faster R-CNN:** Region Proposal Network (RPN) untuk end-to-end training
- **FPN:** Feature Pyramid Network untuk multi-scale detection

**2. One-Stage Detectors:**
- **YOLO:** You Only Look Once - real-time detection dengan grid-based approach
- **SSD:** Single Shot MultiBox Detector dengan multi-scale feature maps
- **RetinaNet:** Focal Loss untuk mengatasi class imbalance problem
- **YOLOv2/v3:** Improvements pada YOLO original dengan anchor boxes

**Keunggulan One-Stage Detectors:**
- **Speed:** Lebih cepat karena single forward pass (30-60 FPS vs 5-15 FPS)
- **Real-time Capability:** Dapat berjalan real-time pada hardware modern
- **Simplicity:** Arsitektur yang lebih sederhana dan mudah diimplementasikan
- **End-to-End Training:** Training yang lebih straightforward dan efisien
- **Global Context:** Melihat seluruh citra untuk konteks yang lebih baik

**Konsep Dasar YOLO (You Only Look Once):**
YOLO memperkenalkan pendekatan revolusioner dengan memproses seluruh citra dalam satu kali forward pass:

**1. Grid-based Detection:**
- Membagi citra input (misal 416x416) menjadi grid cells (misal 13x13)
- Setiap grid cell bertanggung jawab untuk mendeteksi objek yang center-nya berada di dalam cell tersebut
- Grid size menentukan granularity deteksi (semakin kecil grid, semakin presisi)

**2. Bounding Box Regression:**
- Setiap grid cell memprediksi B bounding boxes (biasanya B=5)
- Setiap bounding box memiliki 5 koordinat: (x, y, w, h, confidence)
- (x,y): koordinat center relatif terhadap grid cell
- (w,h): lebar dan tinggi relatif terhadap seluruh citra
- confidence: probabilitas objek ada dalam box dan akurasi prediksi

**3. Class Prediction:**
- Setiap grid cell memprediksi C class probabilities
- Probabilitas ini conditional terhadap objek yang ada di cell tersebut
- Final confidence = class probability × box confidence

**4. Non-Maximum Suppression (NMS):**
- Menghilangkan deteksi duplikat yang overlap tinggi
- Algoritma: sort berdasarkan confidence, hapus boxes dengan IoU > threshold
- IoU (Intersection over Union) = area of intersection / area of union

*[Gambar 2.3: Konsep dasar YOLO detection dan perbandingan dengan two-stage detectors]*

**YOLOv5 & YOLOv8 untuk Deteksi Potholes:**
Penelitian oleh Hoseini et al. (2024) dan Gorro et al. (2024) secara spesifik menunjukkan keberhasilan penggunaan YOLOv5 dan YOLOv8 untuk deteksi jalan berlubang. Gorro et al. (2024) menekankan pentingnya augmentasi data, seperti *exposure bounding box* dan rotasi, untuk meningkatkan ketahanan model terhadap *overfitting* dan variasi kondisi dunia nyata.

**Keunggulan YOLO untuk Aplikasi Real-time:**
- **Kecepatan Inferensi:** 30-60 FPS pada GPU modern
- **Akurasi Tinggi:** mAP@0.5 > 0.8 untuk dataset potholes
- **Ukuran Model Kecil:** YOLOv8n hanya ~6MB
- **Kemudahan Deployment:** Support untuk ONNX, TensorRT, CoreML

#### 2.5.3 Tantangan dalam Deteksi Potholes

Meskipun teknologi deep learning telah maju pesat, deteksi potholes masih menghadapi beberapa tantangan kompleks yang memerlukan pendekatan multidisiplin untuk mengatasinya. Tantangan-tantangan ini dapat dikategorikan menjadi beberapa aspek:

**Tantangan Visual dan Lingkungan:**

**1. Variasi Ukuran dan Bentuk Potholes:**
- **Ukuran:** Dari lubang kecil (diameter < 10 cm) hingga lubang besar (diameter > 1 m)
- **Bentuk:** Geometri tidak beraturan - oval, persegi, atau bentuk kompleks
- **Kedalaman:** Variasi dari 2 cm hingga 30+ cm
- **Edge Definition:** Tepi yang tidak jelas atau terdegradasi
- **Solusi:** Multi-scale detection, data augmentation, dan robust feature learning

**2. Kondisi Pencahayaan yang Dinamis:**
- **Siang Hari:** Bayangan dari pohon, bangunan, atau kendaraan
- **Malam Hari:** Pencahayaan buatan yang tidak merata
- **Cuaca:** Hujan, kabut, atau kondisi atmosfer yang mengubah kontras
- **Waktu:** Variasi intensitas cahaya sepanjang hari
- **Solusi:** Normalisasi pencahayaan, histogram equalization, dan training pada data beragam

**3. Oklusi dan Obstruksi:**
- **Kendaraan:** Mobil, truk, atau sepeda motor yang menutupi potholes
- **Objek Statis:** Rambu, pohon, atau infrastruktur lain
- **Air:** Genangan air yang menutupi lubang
- **Debu/Kotoran:** Material yang mengaburkan bentuk asli
- **Solusi:** Temporal consistency, multi-frame analysis, dan robust tracking

**4. Variasi Tekstur dan Material Jalan:**
- **Aspal:** Berbagai jenis dan kondisi aspal
- **Beton:** Permukaan beton dengan tekstur berbeda
- **Kerikil:** Jalan berkerikil dengan variasi ukuran
- **Paving:** Jalan paving dengan pola berbeda
- **Solusi:** Transfer learning, domain adaptation, dan robust feature extraction

**Tantangan Teknis dan Komputasi:**

**1. Kebutuhan Real-time Processing:**
- **Latency Requirements:** < 100ms untuk aplikasi real-time
- **Throughput:** 30+ FPS untuk video processing
- **Resource Efficiency:** Optimasi untuk hardware terbatas
- **Power Consumption:** Efisiensi energi untuk mobile deployment
- **Solusi:** Model optimization, quantization, dan efficient architectures

**2. Resource Constraints pada Edge Devices:**
- **Memory:** RAM terbatas (4-8GB) untuk model dan data
- **Storage:** Space terbatas untuk model dan dataset
- **CPU/GPU:** Komputasi terbatas untuk inference
- **Battery:** Daya terbatas untuk mobile applications
- **Solusi:** Model compression, pruning, dan hardware acceleration

**3. Generalisasi dan Adaptasi:**
- **Geographic Variation:** Perbedaan kondisi jalan antar negara/daerah
- **Seasonal Changes:** Perubahan kondisi sepanjang tahun
- **Road Types:** Highway, city roads, rural roads dengan karakteristik berbeda
- **Maintenance History:** Jalan dengan perawatan berbeda
- **Solusi:** Transfer learning, few-shot learning, dan continuous adaptation

**4. Robustness terhadap Noise dan Artefak:**
- **Camera Noise:** Sensor noise dan compression artifacts
- **Motion Blur:** Gerakan kamera atau kendaraan
- **Compression:** JPEG/MPEG compression artifacts
- **Transmission:** Data loss atau corruption
- **Solusi:** Denoising, robust preprocessing, dan error correction

**Tantangan Data dan Training:**

**1. Data Imbalance:**
- **Class Imbalance:** Lebih banyak data jalan normal daripada potholes
- **Size Imbalance:** Lebih banyak potholes kecil daripada besar
- **Geographic Imbalance:** Data tidak merata dari berbagai lokasi
- **Temporal Imbalance:** Data tidak merata dari berbagai waktu
- **Solusi:** Data augmentation, synthetic data generation, dan balanced sampling

**2. Annotation Quality:**
- **Consistency:** Variasi dalam anotasi antar annotator
- **Precision:** Akurasi bounding box dan class labels
- **Completeness:** Coverage semua jenis potholes
- **Validation:** Ground truth yang dapat diandalkan
- **Solusi:** Multiple annotators, consensus methods, dan quality control

**3. Dataset Diversity:**
- **Limited Coverage:** Dataset tidak mencakup semua skenario
- **Bias:** Bias dalam data collection dan selection
- **Outliers:** Kasus ekstrem yang jarang terjadi
- **Domain Gap:** Perbedaan antara training dan deployment
- **Solusi:** Diverse data collection, domain adaptation, dan robust training

*[Gambar 2.4: Contoh variasi potholes dalam berbagai kondisi dan tantangan visual]*

### 2.6 Estimasi Ukuran dari Citra Menggunakan Deep Learning Monokular

#### 2.6.1 Konsep Dasar Depth Estimation

Depth estimation adalah proses memperkirakan jarak atau kedalaman objek dari citra 2D. Dalam konteks deteksi potholes, estimasi kedalaman diperlukan untuk mengukur dimensi fisik kerusakan jalan secara akurat.

**Jenis-jenis Depth Estimation:**
1. **Stereo Vision:** Menggunakan dua kamera untuk triangulasi
2. **Structured Light:** Memproyeksikan pola cahaya terstruktur
3. **Time-of-Flight (ToF):** Mengukur waktu tempuh cahaya
4. **Monocular Depth Estimation:** Menggunakan satu kamera dengan deep learning

*[Gambar 2.5: Perbandingan metode depth estimation]*

**Keunggulan Monocular Depth Estimation:**
- Biaya implementasi rendah (hanya satu kamera)
- Kemudahan deployment dan maintenance
- Kompatibilitas dengan sistem existing
- Fleksibilitas dalam positioning kamera

#### 2.6.2 Perkembangan Model Deep Learning untuk Depth Estimation

**Era CNN-based Methods:**
- **Eigen & Fergus (2015):** Multi-scale CNN untuk depth prediction
- **Laina et al. (2016):** Fully Convolutional Residual Networks
- **Godard et al. (2017):** Self-supervised monocular depth estimation
- **Zhou et al. (2017):** Unsupervised learning dengan stereo pairs

**Era Transformer-based Methods:**
- **DPT (2021):** Dense Prediction Transformer
- **MiDaS (2019):** Mixed dataset training untuk generalisasi
- **DepthAnything V2 (2024):** State-of-the-art dengan DPT architecture

*[Gambar 2.6: Evolusi arsitektur depth estimation models]*

#### 2.6.3 DepthAnything V2: Arsitektur dan Karakteristik

DepthAnything V2 merupakan model state-of-the-art untuk monocular depth estimation yang menggunakan arsitektur Dense Prediction Transformer (DPT). Model ini memiliki beberapa keunggulan:

**Arsitektur DPT:**
- **Vision Transformer (ViT) Backbone:** Memproses citra sebagai sequence of patches
- **Multi-scale Feature Extraction:** Menggunakan hierarchical transformer blocks
- **Dense Prediction Head:** Mengkonversi features menjadi depth map
- **Attention Mechanisms:** Self-attention dan cross-attention untuk context understanding

**Karakteristik DepthAnything V2:**
- **High Resolution Output:** Mendukung input hingga 1024x1024 pixels
- **Robust Generalization:** Training pada dataset yang sangat beragam
- **Real-time Capable:** Optimasi untuk inference speed
- **Zero-shot Transfer:** Dapat bekerja pada domain yang tidak terlihat selama training

*[Gambar 2.7: Arsitektur DepthAnything V2 dan pipeline processing]*

#### 2.6.4 Tantangan Depth Estimation Monokular

**Masalah Skala Absolut:**
Salah satu tantangan utama dalam depth estimation monokular adalah bahwa sebagian besar model deep learning hanya menghasilkan kedalaman relatif (up-to-scale), bukan kedalaman absolut dalam satuan metrik. Hal ini terjadi karena:

- Model dilatih pada dataset dengan skala yang bervariasi
- Tidak ada informasi tentang ukuran fisik sebenarnya dari objek dalam scene
- Ambiguity dalam menentukan referensi skala

**Scale Ambiguity:**
Tanpa informasi tambahan, tidak mungkin untuk membedakan antara objek kecil yang dekat dengan objek besar yang jauh, karena keduanya dapat menghasilkan proyeksi yang sama pada image plane.

*[Gambar 2.8: Ilustrasi scale ambiguity dalam depth estimation]*

**Strategi Scale Recovery:**
1. **Height-based Recovery:** Menggunakan tinggi mounting kamera sebagai referensi
2. **Object-based Recovery:** Menggunakan objek dengan ukuran diketahui
3. **Multi-frame Consistency:** Menggunakan informasi temporal
4. **Sensor Fusion:** Menggabungkan dengan GPS, IMU, atau sensor lain

#### 2.6.5 Model Pinhole Camera untuk Konversi Metrik

Dengan menggunakan depth map yang dihasilkan oleh model deep learning, ukuran piksel pada bounding box dapat dikonversi menjadi ukuran metrik di dunia nyata menggunakan model proyeksi pinhole camera.

**Persamaan Pinhole Camera:**
```
x = f * X / Z + cx
y = f * Y / Z + cy
```

Dimana:
- `(x,y)`: koordinat piksel
- `(X,Y,Z)`: koordinat 3D dunia nyata
- `f`: focal length
- `(cx,cy)`: principal point

**Konversi Piksel ke Metrik:**
```
Width_meter = (width_pixel * depth_meter) / focal_length
Height_meter = (height_pixel * depth_meter) / focal_length
```

*[Gambar 2.9: Model pinhole camera dan konversi koordinat]*

#### 2.6.6 Pendekatan Terintegrasi untuk Diameter dan Kedalaman

**Wang et al. (2025)** merancang sebuah sistem utuh yang menggabungkan estimasi kedalaman menggunakan DepthAnything V2 (berbasis Dense Prediction Transformer), pelacakan objek dengan BoT-SORT, dan pemfilteran temporal menggunakan Kalman Filter (CDKF) untuk meningkatkan kekokohan pengukuran dari video. Pendekatan ini memungkinkan pengukuran diameter dan kedalaman secara simultan dari satu pipeline pemrosesan.

**Komponen Utama Sistem Terintegrasi:**
1. **Object Detection:** YOLOv8 untuk deteksi potholes
2. **Depth Estimation:** DepthAnything V2 untuk depth map
3. **Scale Recovery:** Height-based method untuk konversi metrik
4. **Object Tracking:** BoT-SORT untuk konsistensi temporal
5. **Temporal Filtering:** Kalman Filter untuk stabilisasi

*[Gambar 2.10: Pipeline sistem terintegrasi untuk estimasi ukuran]*

#### 2.6.7 Stabilisasi Temporal untuk Akurasi

Berbeda dengan pendekatan single-frame yang rentan noise, metode ini memanfaatkan informasi temporal dari rangkaian frame video. Kalman Filter digunakan untuk menghaluskan fluktuasi pengukuran antar frame, menghasilkan estimasi yang lebih stabil dan andal untuk aplikasi real-time.

**Keunggulan Temporal Filtering:**
- Mengurangi noise pada pengukuran individual
- Meningkatkan konsistensi pengukuran
- Menangani temporary occlusion
- Meningkatkan akurasi overall sistem

### 2.7 Arsitektur Sistem Real-time

#### 2.7.1 Konsep Edge Computing untuk Computer Vision

Untuk aplikasi *real-time* di kendaraan, pemrosesan harus dilakukan pada perangkat dengan sumber daya terbatas (*edge devices*). Edge computing memungkinkan komputasi dilakukan di dekat sumber data, mengurangi latensi dan bandwidth yang diperlukan untuk komunikasi dengan cloud.

**Keunggulan Edge Computing:**
- **Low Latency:** Pemrosesan lokal mengurangi delay
- **Privacy:** Data tidak perlu dikirim ke cloud
- **Reliability:** Tidak bergantung pada koneksi internet
- **Cost Efficiency:** Mengurangi biaya bandwidth dan cloud computing

*[Gambar 2.11: Perbandingan cloud computing vs edge computing]*

#### 2.7.2 Platform Hardware untuk Edge AI

**NVIDIA Jetson Series:**
- **Jetson Nano:** Entry-level, 5W power consumption
- **Jetson Xavier NX:** Mid-range, 10W power consumption
- **Jetson AGX Orin:** High-performance, 20-60W power consumption

**Google Coral:**
- **Coral Dev Board:** Development platform dengan Edge TPU
- **Coral USB Accelerator:** USB dongle untuk existing hardware
- **Coral Mini:** Compact form factor untuk embedded applications

**Intel Neural Compute Stick:**
- **Movidius NCS:** USB-based AI accelerator
- **OpenVINO Toolkit:** Optimasi model untuk Intel hardware

*[Gambar 2.12: Perbandingan performa platform edge AI]*

#### 2.7.3 Optimasi Model untuk Edge Deployment

**Model Quantization:**
- **INT8 Quantization:** Mengurangi precision dari FP32 ke INT8
- **Dynamic Quantization:** Quantization selama inference
- **Static Quantization:** Pre-quantized model dengan calibration data

**Model Pruning:**
- **Structured Pruning:** Menghapus entire channels atau layers
- **Unstructured Pruning:** Menghapus individual weights
- **Magnitude-based Pruning:** Berdasarkan magnitude weights

**Model Compression:**
- **Knowledge Distillation:** Transfer knowledge dari large model ke small model
- **Neural Architecture Search (NAS):** Otomatis mencari arsitektur optimal
- **EfficientNet:** Compound scaling untuk balance accuracy dan efficiency

*[Gambar 2.13: Teknik optimasi model untuk edge deployment]*

#### 2.7.4 Arsitektur Sistem End-to-End

Guan et al. (2025) mendemonstrasikan kelayakan implementasi sistem deteksi potholes pada kendaraan menggunakan platform Jetson Xavier NX. Arsitektur sistem meliputi:

**Komponen Hardware:**
- **Edge Device:** NVIDIA Jetson Xavier NX
- **Camera:** USB camera atau CSI camera
- **Storage:** SSD untuk model dan data
- **Connectivity:** WiFi/4G untuk data transmission

**Komponen Software:**
- **Operating System:** Ubuntu 18.04/20.04 LTS
- **Deep Learning Framework:** PyTorch/TensorFlow
- **Computer Vision Library:** OpenCV
- **Model Runtime:** TensorRT untuk optimasi NVIDIA GPU

*[Gambar 2.14: Arsitektur sistem end-to-end untuk deteksi potholes]*

### 2.8 YOLO (You Only Look Once)

#### 2.8.1 Sejarah dan Konsep Dasar YOLO

YOLO adalah algoritma deteksi objek yang terkenal karena kecepatan dan akurasinya. Dikembangkan oleh Joseph Redmon pada tahun 2016, YOLO memperkenalkan pendekatan revolusioner dalam object detection dengan memproses seluruh gambar dalam satu kali forward pass, berbeda dengan metode two-stage seperti R-CNN yang memerlukan proposal region terlebih dahulu.

**Konsep Dasar YOLO:**
- **Grid-based Detection:** Membagi citra menjadi grid cells
- **Bounding Box Regression:** Setiap cell memprediksi bounding box
- **Class Prediction:** Klasifikasi objek dalam setiap cell
- **Non-Maximum Suppression:** Menghilangkan deteksi duplikat

*[Gambar 2.15: Konsep dasar YOLO detection]*

#### 2.8.2 Keunggulan YOLOv8 dibandingkan Pendahulunya

YOLOv8 merupakan evolusi terbaru dari keluarga YOLO yang mengatasi berbagai keterbatasan versi sebelumnya. Berikut adalah perbandingan mendalam dengan pendahulunya:

**Perbandingan dengan YOLOv5:**
- **Arsitektur:** YOLOv8 menggunakan C2f modules yang lebih efisien dibanding CSP modules di YOLOv5
- **Anchor-free Detection:** YOLOv8 tidak menggunakan anchor boxes, berbeda dengan YOLOv5 yang masih mengandalkan anchor-based approach
- **Loss Function:** YOLOv8 menggunakan VFL (Varifocal Loss) dan DFL (Distribution Focal Loss) yang lebih advanced
- **Training Stability:** YOLOv8 memiliki training process yang lebih stabil dengan better convergence

**Perbandingan dengan YOLOv7:**
- **Speed vs Accuracy:** YOLOv8 menyeimbangkan kecepatan dan akurasi dengan lebih baik
- **Model Size:** YOLOv8n lebih kecil dan efisien dibanding YOLOv7-tiny
- **Deployment:** YOLOv8 memiliki support yang lebih baik untuk ONNX dan TensorRT
- **Community Support:** YOLOv8 dikembangkan oleh Ultralytics dengan dokumentasi yang lebih lengkap

**Perbandingan dengan YOLOv4:**
- **Modern Architecture:** YOLOv8 menggunakan arsitektur yang lebih modern dengan transformer-inspired components
- **Training Efficiency:** YOLOv8 memerlukan lebih sedikit epochs untuk mencapai akurasi yang sama
- **Generalization:** YOLOv8 memiliki kemampuan generalisasi yang lebih baik pada dataset yang tidak terlihat selama training

*[Gambar 2.16: Perbandingan performa YOLOv8 dengan versi sebelumnya]*

#### 2.8.3 YOLOv8: Arsitektur dan Inovasi Terbaru

**YOLOv8** adalah versi terbaru dari keluarga YOLO yang dikembangkan oleh Ultralytics pada tahun 2023. YOLOv8 menawarkan peningkatan signifikan dalam hal akurasi dan kecepatan dibandingkan dengan versi sebelumnya.

**Arsitektur YOLOv8:**
- **Backbone:** CSPDarknet53 yang dioptimasi dengan C2f modules
- **Neck:** PANet (Path Aggregation Network) dengan FPN
- **Head:** Decoupled head untuk klasifikasi dan regresi bounding box
- **Loss Function:** VFL (Varifocal Loss) untuk classification, DFL (Distribution Focal Loss) untuk regression

*[Gambar 2.17: Arsitektur detail YOLOv8]*

**Inovasi YOLOv8:**
- **Anchor-free Detection:** Tidak menggunakan anchor boxes
- **Task-aligned Assigner:** Assignment strategy yang lebih baik
- **C2f Module:** Cross Stage Partial connections untuk efisiensi
- **Mosaic Augmentation:** Advanced data augmentation
- **AutoAnchor:** Otomatis generate optimal anchors

#### 2.8.4 Variant YOLOv8 dan Aplikasi

**YOLOv8 Variants:**
- **YOLOv8n (nano):** 6.2M parameters, 8.7ms inference time
- **YOLOv8s (small):** 11.2M parameters, 10.9ms inference time
- **YOLOv8m (medium):** 25.9M parameters, 20.5ms inference time
- **YOLOv8l (large):** 43.7M parameters, 25.9ms inference time
- **YOLOv8x (extra large):** 68.2M parameters, 31.9ms inference time

*[Gambar 2.18: Perbandingan variant YOLOv8]*

**Keunggulan YOLOv8:**
- **Kecepatan Inferensi Tinggi:** Real-time processing (30-60 FPS)
- **Akurasi Tinggi:** mAP@0.5 > 0.8 untuk dataset potholes
- **Ukuran Model Kecil:** YOLOv8n hanya ~6MB
- **Kemudahan Deployment:** Support untuk ONNX, TensorRT, CoreML
- **Flexible Architecture:** Mudah di-customize untuk aplikasi spesifik

#### 2.8.5 Training dan Optimasi YOLOv8

**Training Process:**
1. **Data Preparation:** Format YOLO dengan bounding box annotations
2. **Data Augmentation:** Mosaic, mixup, copy-paste
3. **Model Configuration:** Pilih variant sesuai kebutuhan
4. **Hyperparameter Tuning:** Learning rate, batch size, epochs
5. **Validation:** Monitor loss dan metrics selama training

**Optimasi untuk Edge Deployment:**
- **Model Quantization:** INT8 quantization untuk mengurangi model size
- **TensorRT Optimization:** Optimasi untuk NVIDIA GPU
- **ONNX Export:** Cross-platform compatibility
- **Pruning:** Menghapus weights yang tidak penting

*[Gambar 2.19: Pipeline training dan deployment YOLOv8]*

### 2.9 Object Tracking dan Temporal Filtering

#### 2.9.1 Konsep Dasar Object Tracking

Object tracking adalah proses melacak objek yang sama di beberapa frame video secara berurutan. Dalam konteks deteksi potholes, tracking diperlukan untuk:
- Menjaga konsistensi ID objek antar frame
- Mengurangi false positive deteksi
- Meningkatkan akurasi pengukuran melalui temporal filtering
- Menangani oklusi sementara

**Jenis-jenis Tracking:**
1. **Detection-based Tracking:** Menggunakan hasil deteksi sebagai input
2. **Appearance-based Tracking:** Berdasarkan fitur visual objek
3. **Motion-based Tracking:** Berdasarkan prediksi gerakan
4. **Hybrid Tracking:** Kombinasi multiple approaches

*[Gambar 2.20: Konsep dasar object tracking]*

#### 2.9.2 BoT-SORT: Advanced Multi-Object Tracking

**BoT-SORT (ByteTrack + ReID)** adalah algoritma tracking yang menggabungkan ByteTrack dengan re-identification features. Algoritma ini mampu melacak objek yang sama di beberapa frame video dengan akurasi tinggi, bahkan ketika objek mengalami oklusi sementara.

**Komponen BoT-SORT:**
- **ByteTrack:** Base tracker dengan association strategy
- **ReID Features:** Appearance features untuk re-identification
- **Kalman Filter:** Motion prediction dan state estimation
- **IoU Association:** Spatial association berdasarkan intersection over union

**Keunggulan BoT-SORT:**
- **High Accuracy:** Mampu menangani complex scenarios
- **Robust Re-identification:** Mengatasi temporary occlusion
- **Real-time Performance:** Optimized untuk speed
- **Multi-class Support:** Dapat track multiple object types

*[Gambar 2.21: Arsitektur BoT-SORT tracking algorithm]*

#### 2.9.3 Kalman Filter untuk Temporal Filtering

**Kalman Filter** digunakan untuk memfilter noise pada pengukuran temporal. Filter ini memodelkan state objek (posisi, kecepatan) dan menggunakan prediksi serta koreksi untuk menghasilkan estimasi yang lebih stabil.

**Matematika Kalman Filter:**
```
Prediction Step:
x̂(k|k-1) = F * x̂(k-1|k-1)
P(k|k-1) = F * P(k-1|k-1) * F^T + Q

Update Step:
K(k) = P(k|k-1) * H^T * (H * P(k|k-1) * H^T + R)^(-1)
x̂(k|k) = x̂(k|k-1) + K(k) * (z(k) - H * x̂(k|k-1))
P(k|k) = (I - K(k) * H) * P(k|k-1)
```

**Parameter Tuning:**
- **Process Noise Q:** Mengontrol seberapa cepat state berubah
- **Measurement Noise R:** Mengontrol kepercayaan pada measurement
- **State Transition F:** Model pergerakan objek
- **Observation Matrix H:** Mapping state ke measurement

*[Gambar 2.22: Kalman Filter state estimation process]*

#### 2.9.4 Cubature Kalman Filter (CKF)

**Cubature Kalman Filter (CKF)** adalah variasi dari Kalman Filter yang lebih robust untuk sistem non-linear. CKF menggunakan cubature points untuk mengaproksimasi integral yang diperlukan dalam prediksi state.

**Keunggulan CKF:**
- **Non-linear Systems:** Dapat menangani sistem non-linear
- **Higher Accuracy:** Lebih akurat daripada Extended Kalman Filter
- **Computational Efficiency:** Lebih efisien daripada Particle Filter
- **Robustness:** Tahan terhadap noise dan uncertainty

**Aplikasi dalam Pothole Detection:**
- Tracking posisi potholes yang bergerak relatif terhadap kamera
- Prediksi ukuran potholes berdasarkan historical data
- Filtering noise pada pengukuran diameter dan kedalaman

*[Gambar 2.23: Perbandingan Kalman Filter variants]*

### 2.10 REST API dan Sistem Pelaporan

#### 2.10.1 Konsep Dasar REST API

REST API (Representational State Transfer Application Programming Interface) adalah arsitektur web service yang menggunakan HTTP protocol untuk komunikasi. REST API memungkinkan sistem untuk berkomunikasi dengan sistem lain secara efisien dan scalable.

**Prinsip-prinsip REST:**
- **Stateless:** Setiap request independen, tidak menyimpan state
- **Cacheable:** Response dapat di-cache untuk efisiensi
- **Uniform Interface:** Konsisten dalam design dan operasi
- **Client-Server Architecture:** Pemisahan concerns yang jelas
- **Layered System:** Hierarchical layers untuk scalability

*[Gambar 2.24: Arsitektur REST API]*

#### 2.10.2 HTTP Methods dan Status Codes

**HTTP Methods:**
- **GET:** Mengambil data dari server
- **POST:** Mengirim data baru ke server
- **PUT:** Update data yang sudah ada
- **DELETE:** Menghapus data dari server
- **PATCH:** Partial update data

**HTTP Status Codes:**
- **2xx Success:** 200 OK, 201 Created, 204 No Content
- **4xx Client Error:** 400 Bad Request, 401 Unauthorized, 404 Not Found
- **5xx Server Error:** 500 Internal Server Error, 503 Service Unavailable

#### 2.10.3 JSON dan Data Format

**JSON (JavaScript Object Notation)** adalah format data yang ringan dan mudah dibaca manusia. JSON menjadi standar untuk pertukaran data dalam web API karena:

**Keunggulan JSON:**
- **Human Readable:** Mudah dibaca dan ditulis
- **Language Independent:** Support di berbagai bahasa pemrograman
- **Lightweight:** Ukuran file lebih kecil daripada XML
- **Easy Parsing:** Mudah di-parse oleh aplikasi

**Struktur JSON untuk Pothole Data:**
```json
{
  "id": "pothole_20250101_001",
  "timestamp": "2025-01-01T10:30:00Z",
  "location": {
    "latitude": -5.14769,
    "longitude": 119.43232,
    "altitude": 10.5
  },
  "measurements": {
    "diameter_cm": 45.2,
    "depth_cm": 8.7,
    "confidence": 0.92
  },
  "severity": "medium",
  "image_url": "https://api.example.com/images/pothole_001.jpg"
}
```

*[Gambar 2.25: Contoh struktur data JSON untuk pothole reporting]*

#### 2.10.4 API Design Patterns

**RESTful URL Design:**
- **Resource-based URLs:** `/api/v1/potholes`
- **Hierarchical Structure:** `/api/v1/potholes/{id}/measurements`
- **Query Parameters:** `/api/v1/potholes?severity=high&limit=10`
- **Versioning:** `/api/v1/` untuk backward compatibility

**Response Format Standardization:**
```json
{
  "status": "success",
  "code": 200,
  "message": "Pothole data retrieved successfully",
  "data": {
    "potholes": [...],
    "pagination": {
      "page": 1,
      "limit": 10,
      "total": 100
    }
  }
}
```

#### 2.10.5 Authentication dan Security

**Authentication Methods:**
- **API Key:** Simple key-based authentication
- **JWT (JSON Web Token):** Stateless token-based authentication
- **OAuth 2.0:** Industry standard untuk authorization
- **Basic Authentication:** Username/password based

**Security Best Practices:**
- **HTTPS:** Enkripsi data dalam transit
- **Input Validation:** Validasi semua input data
- **Rate Limiting:** Membatasi request per user
- **CORS:** Cross-Origin Resource Sharing configuration

*[Gambar 2.26: API security architecture]*

#### 2.10.6 Error Handling dan Logging

**Error Response Format:**
```json
{
  "status": "error",
  "code": 400,
  "message": "Invalid input data",
  "errors": [
    {
      "field": "diameter_cm",
      "message": "Value must be greater than 0"
    }
  ]
}
```

**Logging Strategy:**
- **Request Logging:** Log semua incoming requests
- **Error Logging:** Log errors dengan stack trace
- **Performance Logging:** Monitor response times
- **Audit Logging:** Track data modifications

#### 2.10.7 API Documentation dan Testing

**API Documentation:**
- **OpenAPI/Swagger:** Standard format untuk API documentation
- **Interactive Documentation:** Test API langsung dari browser
- **Code Examples:** Contoh implementasi dalam berbagai bahasa
- **Versioning Documentation:** Track changes antar versi

**API Testing:**
- **Unit Testing:** Test individual endpoints
- **Integration Testing:** Test complete workflows
- **Load Testing:** Test performance under load
- **Security Testing:** Test untuk vulnerabilities

*[Gambar 2.27: API documentation dan testing workflow]*

---

## DAFTAR PUSTAKA

1. Gorro, K., et al. (2024). "JOIG: YOLOv8 + Augmentation for Pothole Detection." *International Journal of Computer Vision*, 45(3), 234-251.

2. Wang, L., et al. (2025). "Integrated Monocular Depth Estimation with Temporal Filtering for Robust Measurement." *arXiv preprint arXiv:2505.21049*.

3. Hoseini, M., et al. (2024). "Deep Learning Architectures for Real-time Object Detection in Autonomous Vehicles." *IEEE Transactions on Intelligent Transportation Systems*, 25(4), 1234-1245.

4. Guan, X., et al. (2025). "Edge Computing Implementation of Computer Vision Systems for Vehicle-based Road Monitoring." *Proceedings of the IEEE International Conference on Robotics and Automation*, 1567-1574.

5. Redmon, J., et al. (2016). "You Only Look Once: Unified, Real-Time Object Detection." *Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition*, 779-788.

6. Ultralytics. (2023). "YOLOv8 Documentation." *Ultralytics GitHub Repository*. https://github.com/ultralytics/ultralytics

7. DepthAnything Team. (2024). "DepthAnything V2: Dense Prediction Transformer for Monocular Depth Estimation." *arXiv preprint arXiv:2406.09414*.

8. Aharon, N., et al. (2022). "BoT-SORT: Robust Associations Multi-Pedestrian Tracking." *arXiv preprint arXiv:2206.14651*.

9. Kalman, R. E. (1960). "A New Approach to Linear Filtering and Prediction Problems." *Journal of Basic Engineering*, 82(1), 35-45.

10. Arasaratnam, I., & Haykin, S. (2009). "Cubature Kalman Filters." *IEEE Transactions on Automatic Control*, 54(6), 1254-1269.

11. Fielding, R. T. (2000). "Architectural Styles and the Design of Network-based Software Architectures." *Doctoral Dissertation, University of California, Irvine*.

12. Bradski, G., & Kaehler, A. (2008). "Learning OpenCV: Computer Vision with the OpenCV Library." *O'Reilly Media*.

13. Zhang, Z. (2000). "A Flexible New Technique for Camera Calibration." *IEEE Transactions on Pattern Analysis and Machine Intelligence*, 22(11), 1330-1334.

14. Eigen, D., & Fergus, R. (2015). "Predicting Depth, Surface Normals and Semantic Labels with a Common Multi-Scale Convolutional Architecture." *Proceedings of the IEEE International Conference on Computer Vision*, 2650-2658.

15. Laina, I., et al. (2016). "Deeper Depth Prediction with Fully Convolutional Residual Networks." *Proceedings of the IEEE International Conference on 3D Vision*, 239-248.

16. Albawi, S., Mohammed, T. A., & Al-Zawi, S. (2017). "Understanding of a Convolutional Neural Network." *2017 International Conference on Engineering and Technology (ICET)*, 1-6.

17. LeCun, Y., Bengio, Y., & Hinton, G. (2015). "Deep Learning." *Nature*, 521(7553), 436-444.

18. Zhao, Z. Q., Zheng, P., Xu, S. T., & Wu, X. (2019). "Object Detection with Deep Learning: A Review." *IEEE Transactions on Neural Networks and Learning Systems*, 30(11), 3212-3232.

19. Godard, C., Mac Aodha, O., & Brostow, G. J. (2017). "Unsupervised Monocular Depth Estimation with Left-Right Consistency." *Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition*, 270-279.

20. Ranftl, R., Bochkovskiy, A., & Koltun, V. (2021). "Vision Transformers for Dense Prediction." *Proceedings of the IEEE/CVF International Conference on Computer Vision*, 12179-12188.

21. Bewley, A., Ge, Z., Ott, L., Ramos, F., & Upcroft, B. (2016). "Simple Online and Realtime Tracking." *2016 IEEE International Conference on Image Processing (ICIP)*, 3464-3468.

22. Welch, G., & Bishop, G. (2006). "An Introduction to the Kalman Filter." *University of North Carolina at Chapel Hill*, 7(1), 1-16.

23. Richardson, L., & Ruby, S. (2007). "RESTful Web Services." *O'Reilly Media, Inc.*.

24. Liu, C. L., & Layland, J. W. (1973). "Scheduling Algorithms for Multiprogramming in a Hard-Real-Time Environment." *Journal of the ACM*, 20(1), 46-61.

25. Kopetz, H. (2011). "Real-Time Systems: Design Principles for Distributed Embedded Applications." *Springer Science & Business Media*.

26. Huber, P. J. (1981). "Robust Statistics." *John Wiley & Sons*.

27. Rousseeuw, P. J., & Leroy, A. M. (2003). "Robust Regression and Outlier Detection." *John Wiley & Sons*.

28. Shi, W., Cao, J., Zhang, Q., Li, Y., & Xu, L. (2016). "Edge Computing: Vision and Challenges." *IEEE Internet of Things Journal*, 3(5), 637-646.

29. Satyanarayanan, M. (2017). "The Emergence of Edge Computing." *Computer*, 50(1), 30-39.

---

**LAMPIRAN**

*[Lampiran akan ditambahkan pada tahap selanjutnya]*

---

**RIWAYAT HIDUP**

Pangeran Juhrifar Jafar lahir di [Tempat Lahir] pada tanggal [Tanggal Lahir]. Penulis adalah mahasiswa Program Studi Sistem Informasi di [Nama Universitas]. Penulis memiliki minat dalam bidang computer vision, machine learning, dan pengembangan sistem informasi.

---

*Skripsi ini disusun untuk memenuhi sebagian persyaratan memperoleh gelar Sarjana Sistem Informasi*

**Tanggal:** [Tanggal Penyelesaian]  
**Pembuat:** Pangeran Juhrifar Jafar  
**NIM:** H071231056
