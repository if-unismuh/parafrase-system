# Full Gemini Paraphraser v2.0 - Large File Support

## Fitur Baru untuk File Besar

### 🚀 Peningkatan Utama

1. **Chunking Otomatis**: Memotong teks besar menjadi potongan yang dapat dikelola
2. **Rate Limiting Cerdas**: Menangani batas API Gemini secara adaptif
3. **Progress Tracking**: Menyimpan kemajuan proses untuk file besar
4. **Resume Capability**: Melanjutkan proses yang terputus
5. **Error Recovery**: Retry otomatis dengan exponential backoff

### 📏 Konfigurasi untuk File Besar

```python
# Inisialisasi untuk file besar
paraphraser = FullGeminiParaphraser(
    synonym_file='sinonim.json',
    chunk_size=3000,        # Ukuran chunk (characters)
    max_retries=5           # Maksimal retry per request
)
```

### 🔄 Cara Menggunakan

#### 1. Proses Normal (dengan Resume Otomatis)
```bash
python full_gemini_paraphraser.py
```

#### 2. Demo untuk File Besar
```bash
python full_gemini_paraphraser.py demo
```

#### 3. Resume Proses Terputus
```bash
python full_gemini_paraphraser.py resume
```

#### 4. Cek Status Pending
```bash
python full_gemini_paraphraser.py check
```

#### 5. Proses File Tunggal dengan Chunk Custom
```bash
python full_gemini_paraphraser.py single "documents/file_besar.docx" 2000
```

### 📊 Fitur Progress Tracking

Sistem akan membuat folder `progress/` yang berisi:
- `filename_progress.json`: Status kemajuan setiap dokumen
- Informasi paragraf yang sudah selesai
- Waktu terakhir diupdate
- Statistik proses

### ⚡ Rate Limiting & Error Handling

#### Rate Limiting Adaptif
- **Base delay**: 1 detik antar request
- **Content-based**: Delay lebih lama untuk konten besar
- **Adaptive**: Mengurangi delay jika sukses, menambah jika error
- **Exponential backoff**: 2^attempt untuk retry

#### Error Recovery
- **HTTP 429 (Rate Limit)**: Auto-retry dengan delay yang diperbesar
- **HTTP 503 (Service Unavailable)**: Retry dengan backoff
- **Network errors**: Retry dengan exponential delay
- **Keyboard interrupt**: Simpan progress dan exit gracefully

### 🧩 Text Chunking

```python
def split_large_text(self, text):
    # Memotong teks berdasarkan batas kalimat
    # Mempertahankan struktur dan konteks
    # Ukuran maksimal sesuai chunk_size
```

**Keunggulan:**
- Mempertahankan batas kalimat
- Tidak memotong di tengah kata
- Menjaga konteks paragraph
- Menggabungkan hasil chunks dengan natural

### 💾 Progress Persistence

File progress menyimpan:
```json
{
  "input_path": "documents/skripsi.docx",
  "output_path": "completed/skripsi_paraphrased.docx",
  "total_paragraphs": 150,
  "completed_paragraphs": [0, 1, 2, 15, 16],
  "results": [...],
  "start_time": "2025-08-13T10:30:00",
  "last_update": "2025-08-13T10:45:00"
}
```

### 🎯 Optimasi untuk File Besar

#### Chunk Size Recommendations:
- **File kecil** (< 50 paragraf): `chunk_size=5000`
- **File sedang** (50-200 paragraf): `chunk_size=3000-4000`
- **File besar** (> 200 paragraf): `chunk_size=2000-3000`

#### Rate Limiting Settings:
- **Koneksi stabil**: `rate_limit_delay=0.5`
- **Koneksi lambat**: `rate_limit_delay=2.0`
- **API key shared**: `rate_limit_delay=3.0`

### 🛡️ Penanganan Gangguan

#### Jika Proses Terputus:
1. **Ctrl+C**: Progress disimpan otomatis
2. **Network error**: Progress disimpan setiap 5 paragraf
3. **API limit**: Progress disimpan dan retry otomatis

#### Melanjutkan Proses:
1. Jalankan script lagi dengan `resume=True` (default)
2. Sistem otomatis mendeteksi file progress
3. Melanjutkan dari paragraf terakhir yang berhasil

### 📈 Monitoring & Statistics

```python
# Statistik real-time
{
    'runtime': '0:15:30',
    'total_api_calls': 45,
    'total_tokens_used': 15000,
    'paragraphs_processed': 42,
    'protected_content': 3,
    'average_quality': 87.5,
    'total_similarity_reduction': 65.2
}
```

### ⚠️ Tips untuk File Sangat Besar

1. **Gunakan chunk_size kecil** (2000-3000 characters)
2. **Set max_retries tinggi** (5-10)
3. **Monitor progress** dengan command `check`
4. **Backup file asli** sebelum proses
5. **Pastikan koneksi internet stabil**
6. **Proses di waktu off-peak** untuk API yang lebih stabil

### 🔧 Troubleshooting

#### Problem: API Rate Limit
**Solution**: 
- Perbesar `rate_limit_delay`
- Kurangi `chunk_size`
- Gunakan API key berbeda

#### Problem: Proses Lambat
**Solution**:
- Optimalkan `chunk_size`
- Cek koneksi internet
- Monitor penggunaan API quota

#### Problem: Out of Memory
**Solution**:
- Kurangi `chunk_size`
- Proses file satu per satu
- Restart script secara berkala

### 📋 Command Summary

| Command | Fungsi |
|---------|--------|
| `python full_gemini_paraphraser.py` | Proses semua file dengan auto-resume |
| `python full_gemini_paraphraser.py demo` | Demo dengan interaksi user |
| `python full_gemini_paraphraser.py resume` | Resume semua file pending |
| `python full_gemini_paraphraser.py check` | Cek status file pending |
| `python full_gemini_paraphraser.py single <file> [chunk]` | Proses file tunggal |

Sistem ini dirancang khusus untuk mengatasi batasan API Gemini dan memastikan file besar dapat diproses dengan sukses tanpa gangguan.