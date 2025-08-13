# 📖 Core Chapters Processing Guide

## ✨ Fitur Baru: Proses Hanya BAB I - BAB V

Sistem sekarang dapat memproses **hanya konten inti skripsi** (BAB I PENDAHULUAN sampai BAB V KESIMPULAN) dan **mengabaikan** bagian-bagian yang tidak perlu seperti:

❌ **Yang Diabaikan:**
- Cover page / halaman judul
- Halaman persetujuan
- Kata pengantar
- Daftar isi
- Daftar pustaka/references
- Lampiran/appendices

✅ **Yang Diproses:**
- BAB I PENDAHULUAN
- BAB II (Literature Review/Tinjauan Pustaka)
- BAB III (Metodologi)
- BAB IV (Hasil dan Pembahasan)
- BAB V KESIMPULAN/PENUTUP

## 🚀 Cara Penggunaan

### 1. Proses Semua File (Core Chapters Saja)
```bash
python full_gemini_paraphraser.py core
```

### 2. Proses File Tunggal (Core Chapters Saja)  
```bash
python full_gemini_paraphraser.py core-single "documents/skripsi.docx"
```

### 3. Demo dan Test
```bash
python demo_core_chapters.py
```

## 📊 Contoh Hasil Deteksi

**File**: SKRIPSI FAHRISAL FADLI-2.docx
- ✅ **Start**: BAB I PENDAHULUAN (paragraph 245)
- ✅ **End**: BAB V PENUTUP (paragraph 272)
- 📄 **Core content**: 27 paragraphs saja (vs 701 total paragraphs)
- ⚡ **Estimasi waktu**: 5-10 menit (vs 2-3 jam untuk full document)

## 🎯 Keunggulan Core Chapters Processing

### ⚡ **Efisiensi Waktu**
- Proses 27 paragraphs vs 701 paragraphs
- Waktu: ~10 menit vs ~3 jam
- API calls: ~30 vs ~700

### 💰 **Hemat Biaya**
- Penggunaan API Gemini berkurang ~90%
- Token usage lebih efisien
- Rate limiting issues minimal

### 🎯 **Fokus Konten**
- Hanya parafrase konten akademik penting
- Skip bagian administratif
- Output lebih bersih dan relevan

### 📁 **Output Terorganisir**
- File output: `namafile_core_chapters_paraphrased.docx`
- Hanya berisi BAB I-V yang sudah diparafrase
- Mudah untuk digabungkan dengan bagian lain jika diperlukan

## 🔧 Konfigurasi Optimal

```python
# Untuk core chapters, gunakan setting ini:
paraphraser = FullGeminiParaphraser(
    chunk_size=3000,    # Lebih kecil untuk stabilitas
    max_retries=3,      # Cukup untuk core content
    rate_limit_delay=1.0 # Standard delay
)
```

## 📋 Pattern Detection

Sistem mendeteksi otomatis:

**Mulai dari:**
- `BAB I PENDAHULUAN`
- `BAB 1 PENDAHULUAN`
- `CHAPTER I PENDAHULUAN`
- `1. PENDAHULUAN`

**Berakhir di:**
- `BAB V KESIMPULAN`
- `BAB V PENUTUP`
- `DAFTAR PUSTAKA`
- `REFERENCES`
- `LAMPIRAN`
- `APPENDIX`

## ⚠️ Tips Penggunaan

1. **Pastikan Format BAB Standar**
   - Gunakan "BAB I", "BAB II", dst.
   - Atau "BAB 1", "BAB 2", dst.
   - Include kata "PENDAHULUAN" untuk BAB I

2. **File Structure**
   ```
   documents/
   ├── skripsi1.docx
   ├── skripsi2.docx
   └── ...
   
   completed/
   ├── skripsi1_core_chapters_paraphrased.docx
   ├── skripsi2_core_chapters_paraphrased.docx
   └── ...
   ```

3. **Monitoring Progress**
   - Progress real-time ditampilkan
   - Jika terputus, gunakan resume function
   - Log disimpan untuk troubleshooting

## 🎉 Workflow Optimal

1. **Deteksi Chapter**: Otomatis detect BAB I-V
2. **Preview**: Lihat berapa paragraphs yang akan diproses
3. **Proses**: Hanya proses core content
4. **Output**: File bersih berisi BAB I-V saja
5. **Manual Combine**: Gabungkan dengan cover/appendix jika perlu

## 📞 Troubleshooting

**Q: Tidak detect BAB I?**
A: Pastikan ada text "BAB I" atau "BAB 1" followed by "PENDAHULUAN"

**Q: Proses terlalu lama?**
A: Core chapters seharusnya cepat. Check koneksi internet dan API key.

**Q: Output tidak lengkap?**  
A: Check detection boundaries dengan demo script dulu.

**Q: Ingin include appendix?**
A: Gunakan mode normal (`python full_gemini_paraphraser.py`) instead of core mode.

---

**🎯 Kesimpulan**: Mode core chapters sangat cocok untuk parafrase cepat dan efisien pada konten akademik inti skripsi, menghemat waktu dan biaya API secara signifikan.