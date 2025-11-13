# 🖨️ Panduan Print Checkerboard Pattern

## ⚠️ PENTING: Print dengan Ukuran Aktual!

**Yang paling penting:** Print dengan **"Actual Size"** atau **"100% Scale"**, BUKAN "Scale to Fit" atau "Fit to Page". Jika tidak, ukuran kotak tidak akan tepat 25mm dan kalibrasi akan salah!

---

## 📋 Metode 1: Print Langsung dari Windows (Recommended)

### Langkah-langkah:

1. **Buka file checkerboard** (`checkerboard_a4.png`)
   - Klik kanan → Open with → Photos / Paint / Image Viewer

2. **Buka Print Dialog**
   - Tekan `Ctrl + P` atau klik Print

3. **Setting Printer (PENTING!):**
   - ✅ **Paper size:** A4 (210mm × 297mm)
   - ✅ **Scale:** **"Actual Size"** atau **"100%"** (BUKAN "Fit to Page")
   - ✅ **Quality:** High / Best Quality
   - ✅ **Color:** Black & White (atau Grayscale)
   - ✅ **Orientation:** Portrait (untuk A4 7×10)

4. **Preview sebelum print:**
   - Pastikan checkerboard tidak terpotong
   - Jika terpotong, cek margin settings

5. **Print!**

---

## 📋 Metode 2: Print via PDF (Lebih Akurat)

### Langkah-langkah:

1. **Buka file PNG** di image viewer

2. **Print to PDF:**
   - Tekan `Ctrl + P`
   - Pilih printer: **"Microsoft Print to PDF"** atau **"Save as PDF"**
   - Setting: **Actual Size / 100%**
   - Save sebagai PDF

3. **Buka PDF** dan print:
   - Buka PDF dengan Adobe Reader / Edge
   - Print dengan setting:
     - ✅ **Page Scaling:** None / Actual Size
     - ✅ **Auto-rotate:** Off
     - ✅ **Paper size:** A4

---

## 📋 Metode 3: Menggunakan Image Editor (GIMP/Photoshop)

### Langkah-langkah:

1. **Buka file** di GIMP / Photoshop

2. **Set Document Size:**
   - Image → Print Size
   - Set resolution: **300 DPI** (atau sesuai DPI yang digunakan saat generate)
   - Set width/height sesuai ukuran yang di-generate

3. **Print:**
   - File → Print
   - Scale: **100%** atau **Actual Size**

---

## ✅ Verifikasi Setelah Print

**PENTING:** Setelah print, **WAJIB verifikasi** ukuran kotak!

### Cara Verifikasi:

1. **Ukur dengan penggaris:**
   - Ukur salah satu kotak hitam/putih
   - Harus tepat **25mm × 25mm** (atau sesuai yang digunakan)
   - Jika tidak tepat, print ulang dengan setting yang benar!

2. **Tips verifikasi cepat:**
   - 4 kotak = 100mm
   - 8 kotak = 200mm
   - Gunakan ini untuk quick check

### Jika Ukuran Tidak Tepat:

- ❌ **Kotak terlalu kecil:** Printer menggunakan "Fit to Page" → Print ulang dengan "Actual Size"
- ❌ **Kotak terlalu besar:** Scale setting salah → Print ulang dengan "100%"
- ❌ **Pattern terpotong:** Margin terlalu besar → Kurangi margin atau gunakan kertas lebih besar

---

## 🎯 Tips untuk Hasil Terbaik

### 1. **Kualitas Print:**
- ✅ Gunakan printer dengan resolusi tinggi (minimal 300 DPI)
- ✅ Gunakan kertas foto atau kertas tebal (tidak mudah melengkung)
- ✅ Print dengan kualitas terbaik (Best Quality)

### 2. **Kertas:**
- ✅ Gunakan kertas A4 berkualitas baik
- ✅ Pastikan kertas datar (tidak melengkung/keriput)
- ✅ Hindari kertas glossy yang terlalu mengkilap (bisa menyebabkan refleksi)

### 3. **Setelah Print:**
- ✅ Tempelkan ke papan/kardus yang keras dan datar
- ✅ Pastikan tidak ada lipatan atau lengkungan
- ✅ Simpan di tempat datar (jangan digulung)

---

## 📐 Ukuran yang Diharapkan

### Untuk Pattern A4 (7×10 internal corners, 25mm):
- **Total squares:** 8×11 squares
- **Total ukuran:** 200mm × 275mm
- **Ukuran kotak:** 25mm × 25mm
- **Margin A4:** ~5mm di setiap sisi (untuk muat di A4 210mm × 297mm)

### Untuk Pattern Standar (9×6 internal corners, 25mm):
- **Total squares:** 10×7 squares
- **Total ukuran:** 250mm × 175mm
- **Ukuran kotak:** 25mm × 25mm
- **Perlu kertas:** Lebih besar dari A4 (bisa print di A3 atau kertas khusus)

---

## 🔧 Troubleshooting

### Problem: Pattern terpotong saat print
**Solusi:**
- Cek margin settings (set ke minimum)
- Pastikan paper size sesuai (A4 untuk pattern A4)
- Coba print via PDF dulu untuk preview

### Problem: Ukuran kotak tidak tepat setelah print
**Solusi:**
- Pastikan print dengan "Actual Size" / "100%"
- Jangan gunakan "Scale to Fit" atau "Fit to Page"
- Verifikasi DPI setting (harus 300 DPI jika generate dengan --dpi 300)

### Problem: Pattern buram/tidak jelas
**Solusi:**
- Print dengan kualitas terbaik
- Gunakan printer dengan resolusi tinggi
- Cek apakah printer perlu cleaning

### Problem: Kertas melengkung setelah print
**Solusi:**
- Gunakan kertas tebal (photo paper atau cardstock)
- Tempelkan ke papan/kardus yang keras
- Simpan di tempat datar

---

## ✅ Checklist Sebelum Kalibrasi

- [ ] Checkerboard sudah di-print dengan ukuran aktual (Actual Size)
- [ ] Ukuran kotak sudah diverifikasi dengan penggaris (tepat 25mm)
- [ ] Pattern tidak terpotong
- [ ] Kertas datar (tidak melengkung)
- [ ] Pattern jelas dan tidak buram
- [ ] Pattern sudah ditempelkan ke papan yang keras (opsional tapi disarankan)

---

## 📝 Catatan Penting

1. **Ukuran kotak HARUS tepat** - ini kritis untuk kalibrasi metrik yang akurat
2. **Pattern harus datar** - lengkungan akan menyebabkan error kalibrasi
3. **Kualitas print harus baik** - pattern buram akan sulit dideteksi oleh OpenCV
4. **Simpan pattern dengan baik** - jangan sampai rusak/lengkung sebelum digunakan

---

**Setelah print dan verifikasi, checkerboard siap digunakan untuk kalibrasi kamera!** 🎯

