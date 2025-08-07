# 🚀 Sistem Parafrase Terintegrasi

## 📖 Deskripsi
Sistem parafrase lengkap dengan deteksi plagiarisme online dan offline, paraphrasing otomatis, dan manajemen dokumen.

## ⚡ Quick Start

### Metode 1: Launcher (Recommended)
```bash
python main.py
```

### Metode 2: Direct Run
```bash
python integrated_smart_paraphrase_system.py
```

## 📁 Struktur Folder

```
📂 parafrase-system/
├── 🚀 main.py                                    (Launcher)
├── 🏆 integrated_smart_paraphrase_system.py      (Sistem Utama)
├── 📂 components/                                (Komponen Inti)
│   ├── ultimate_hybrid_paraphraser.py
│   ├── smart_plagiarism_checker.py
│   ├── plagiarism_detector.py
│   └── sinonim.json
├── 📂 documents/                                 (Input Dokumen) 
├── 📂 completed/                                 (Hasil Akhir)
├── 📂 backups/                                   (Backup Otomatis)
├── 📂 archive/                                   (File Lama)
├── 📂 tests/                                     (File Testing)
└── 📂 docs/                                      (Dokumentasi)
```

## 🎯 Fitur Utama

- ✅ **Deteksi Plagiarisme Online** - Cek similarity dengan sumber internet
- ✅ **Analisis Pattern** - Deteksi pola akademik berbahaya
- ✅ **Parafrase AI** - Smart paraphrasing dengan multiple modes
- ✅ **Auto Backup** - Backup otomatis dokumen asli
- ✅ **Completed Folder** - Hasil siap compare (original vs paraphrased)
- ✅ **Comprehensive Reports** - Laporan JSON detail

## 🔧 Workflow

1. **Input**: Letakkan dokumen di `documents/` folder
2. **Detection**: Sistem scan plagiarisme online + pattern
3. **Analysis**: Identifikasi paragraf berisiko tinggi
4. **Paraphrasing**: Auto-parafrase bagian berbahaya
5. **Output**: Dokumen hasil + original di `completed/` folder

## 🏆 Sistem Utama

### `integrated_smart_paraphrase_system.py`
- Sistem terlengkap dan terbaru
- Menggabungkan semua fitur dalam satu workflow
- User-friendly dengan auto-selection
- Production ready

### Mode Processing:
- **Smart Mode**: Efficient, cost-optimized
- **Balanced Mode**: Best quality, balanced approach  
- **Aggressive Mode**: Maximum plagiarism reduction
- **Turnitin-Safe Mode**: Extra careful untuk Turnitin

## 📊 Komponen Pendukung

### `components/ultimate_hybrid_paraphraser.py`
- Core paraphrasing engine
- Local + AI hybrid approach
- Multiple operation modes
- Smart routing logic

### `components/plagiarism_detector.py`
- Online plagiarism detection
- Academic database integration
- Indonesian repository support
- Real-time similarity checking

### `components/smart_plagiarism_checker.py`
- Offline pattern analysis
- Academic writing pattern detection
- No internet required
- Fast local processing

## 📈 Output Files

### Completed Folder:
```
📂 completed/
├── 📄 DOCUMENT_ORIGINAL_20250807_123456.docx
└── 🤖 DOCUMENT_paraphrased_20250807_123456.docx
```

### Reports:
- `combined_analysis_[timestamp].json` - Analisis gabungan
- `paraphrase_report_[timestamp].json` - Detail paraphrasing
- `integrated_analysis_report_[timestamp].json` - Laporan lengkap

## 🔧 Requirements

```bash
pip install python-docx requests beautifulsoup4 google-generativeai python-dotenv
```

## 🚀 Usage Examples

### Basic Usage:
```bash
python main.py
# Select option 1 for full system
```

### Advanced Usage:
```python
from integrated_smart_paraphrase_system import IntegratedSmartParaphraseSystem

system = IntegratedSmartParaphraseSystem(mode='smart')
result = system.process_document_complete('document.docx', auto_paraphrase=True)
```

## 📋 File Archive

File-file lama tersimpan di folder `archive/` untuk referensi historical:
- `paraphrase_system.py` - Sistem original
- `main_paraphrase_system.py` - Versi lama  
- `smart_hybrid_paraphraser.py` - V2 hybrid
- Dan lainnya...

## 💡 Tips

1. **Letakkan dokumen utama** di folder `documents/` untuk prioritas tinggi
2. **Check completed folder** setelah processing untuk comparison
3. **Review highlights** pada dokumen hasil parafrase
4. **Simpan backup** yang dibuat otomatis sistem
5. **Gunakan mode aggressive** untuk dokumen dengan risiko tinggi

## ⚠️ Catatan

- File di `archive/` adalah versi lama dan tidak direkomendasikan
- Gunakan `integrated_smart_paraphrase_system.py` untuk semua kebutuhan
- Sistem memerlukan koneksi internet untuk deteksi online plagiarisme
- AI paraphrasing memerlukan Gemini API key (opsional)

---
📧 **Support**: Check SYSTEM_ANALYSIS.md untuk detail teknis lengkap
