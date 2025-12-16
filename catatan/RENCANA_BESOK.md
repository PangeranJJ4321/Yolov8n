# 📅 RENCANA GENTING: FINAL PUSH (Deadline 23:59 Besok)

## 🌄 Sesi Pagi: Validasi Data (07:00 - 10:00)

Target: Mendapatkan 1 video valid dengan "Ground Truth" untuk membungkam keraguan reviewer soal akurasi depth.

### 1. Persiapan Alat

- [X] Laptop + Script `api.py` (untuk tes deteksi on-site jika memungkinkan, atau rekam dulu proses nanti).
- [X] **Kamera HP** (yang dipake kalibrasi!).
- [X] **Meteran Bangunan** (Roll meter).
- [X] **Objek Pembanding** (opsional): Kertas A4 atau kotak rokok untuk referensi skala visual.
- [X] **Lakban/Kapur** (untuk tandai lokasi lubang).

### 2. Prosedur Rekam Video

- [ ] Cari jalan sepi dan **rata** (untuk validasi *flat ground assumption*).
- [ ] Pilih 1 Lubang Jalan yang "Cantik" (tepian jelas, ada kedalaman).
- [ ] **UKUR MANUAL (Ground Truth):**
  - [ ] Diameter Panjang (cm).
  - [ ] Diameter Lebar (cm).
  - [ ] Kedalaman Maksimum (cm) - *PENTING!* (Tusuk penggaris ke titik terdalam).
  - [ ] Foto hasil ukur manual sebagai bukti (untuk dilampirkan kalau perlu).
- [ ] **SETTING KAMERA:**
  - [ ] Ukur tinggi HP dari tanah ($H_{cam}$) saat memegang. Usahakan **stabil 150cm** (1.5m) atau angka pasti lainnya.
  - [ ] Pastikan posisi kamera tegak lurus (hindari terlalu nunduk/dongak).
- [ ] **ACTION:**
  - [X] Rekam video mendekati lubang (seperti mobil jalan pelan). Durasi 10-15 detik cukup.
  - [X] Gerakan harus *smooth* (jangan goyang parah).

---

## ☀️ Sesi Siang: Integrasi & Analisis (11:00 - 14:00)

Target: Mengganti data "dummy" atau "asumsi" di paper dengan data nyata dari pagi.

### 1. Proses Video Baru

- [ ] Pindahkan video ke `d:\PANGERAN\rsic\Yolov8n\test_videos\final_test.mp4`.
- [ ] Update config di `test_integration.py` (sesuaikan $H_{cam}$ dengan yang diukur pagi).
- [ ] Jalankan `test_integration.py`.
- [ ] Ambil output JSON (`pothole_video_measurements.json`).

### 2. Update Grafik

- [ ] Jalankan `src/analyze_results.py` lagi.
- [ ] Cek folder `analysis_plots`. Apakah histogram/scatter plot masuk akal?
- [ ] Copy gambar baru ke folder paper.

### 3. Update Paper (Bab 3 & 4)

- [ ] Buka `paper1.4.tex`.
- [ ] Bagian **Metodologi**: Update jika ada prosedur pengambilan data yang unik.
- [ ] Bagian **Hasil - Akurasi**:
  - [ ] Masukkan Tabel Perbandingan: **"Pengukuran Manual vs Estimasi Sistem"**.
  - [ ] Hitung Error Absolut (dalam cm) dan Error Relatif (%).
  - [ ] *Jujur saja kalau masih ada error, tapi bahas "KENAPA" (itu nilai akademisnya).*

---

## 🌆 Sesi Sore: Finalisasi Dokumen (15:00 - 18:00)

Target: Dokumen siap submit, bahasa baku, format rapi.

- [ ] **Proofreading Abstrak**: Pastikan klaim sesumbar ("Real-time", "Akurasi") sudah direm sesuai hasil siang.
- [ ] **Cek Referensi**: Apakah semua citasi `\cite{}` muncul di Daftar Pustaka?
- [ ] **Layouting**: Cek posisi Gambar/Tabel. Jangan sampai kepotong atau loncat halaman aneh.
- [ ] **Kirim ke Reviewer** (Teman/Dosen) untuk cek typo bahasa Indonesia.

---

## 🌙 Sesi Malam: SUBMISSION (19:00 - 23:59)

- [ ] Compile PDF Final.
- [ ] Cek ulang nama penulis, afiliasi, email.
- [ ] Berdoa & Submit! 🚀

---

### ⚠️ Catatan Kritis:

> Jangan habiskan waktu ngoding fitur tambahan (Web UI dll) besok pagi. **FOKUS KE DATA & PAPER.** Web UI yang sekarang sudah cukup untuk demo/screenshot.
