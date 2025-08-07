# 🎯 Sistem Deteksi Parafrase - Cara Kerja Deteksi Turnitin Risk

## 📊 Overview Sistem Deteksi

Sistem parafrase menggunakan **multi-layer detection** untuk menentukan apakah sebuah paragraf perlu diparafrase dan seberapa agresif parafrase yang diperlukan.

---

## 🔍 1. ENHANCED TURNITIN RISK DETECTION

### 📍 Fungsi Utama: `detect_enhanced_turnitin_risk()`

```python
def detect_enhanced_turnitin_risk(self, text):
    """Enhanced risk detection with more granular analysis"""
    risk_score = 0.0
    detected_patterns = []
    pattern_details = {}
    
    text_lower = text.lower()
```

### 🎯 5 Kategori Pattern Detection:

#### 1️⃣ **Academic Templates (Risk Tertinggi)**
```python
# Pattern yang sering dideteksi Turnitin dari PDF yang dianalisis
academic_templates = [
    'menurut pendapat',
    'berdasarkan teori',
    'dalam penelitian ini',
    'hasil penelitian menunjukkan',
    'dapat disimpulkan bahwa',
    'sesuai dengan pendapat',
    'seperti yang dikemukakan'
]
```

#### 2️⃣ **Technical Definitions (Risk Sangat Tinggi)**
```python
# Definisi teknis yang heavily flagged di PDF
technical_definitions = [
    'definisi sistem',
    'pengertian metode',
    'konsep dasar',
    'teori yang mendasari',
    'prinsip kerja',
    'karakteristik utama'
]
```

#### 3️⃣ **Citation Patterns**
```python
# Pola sitasi yang mudah dideteksi
citation_patterns = [
    r'\(\d{4}\)',           # (2023)
    r'et al\.',             # et al.
    r'vol\. \d+',           # vol. 1
    r'no\. \d+',            # no. 2
    r'hal\. \d+',           # hal. 15
    r'p\. \d+'              # p. 25
]
```

#### 4️⃣ **Methodology Patterns**
```python
# Pola metodologi penelitian
methodology_patterns = [
    'metode penelitian',
    'teknik pengumpulan data',
    'analisis data',
    'populasi dan sampel',
    'instrumen penelitian',
    'uji validitas'
]
```

#### 5️⃣ **Domain Terms Density**
```python
# Kepadatan istilah domain
domain_terms = [
    'sistem informasi', 'database', 'algoritma',
    'penelitian', 'analisis', 'implementasi',
    'evaluasi', 'metodologi', 'framework'
]
```

---

## 📈 2. RISK SCORE CALCULATION

### 🧮 Formula Perhitungan Risk:

```python
# Setiap kategori memiliki bobot berbeda
risk_score += academic_matches * 0.3      # 30% weight
risk_score += technical_matches * 0.25    # 25% weight  
risk_score += citation_matches * 0.2      # 20% weight
risk_score += methodology_matches * 0.15  # 15% weight
risk_score += domain_density * 0.1        # 10% weight

# Normalisasi ke 0-1
risk_level = min(risk_score, 1.0)
```

### 🎯 Kategori Risk Level:

```python
def get_enhanced_risk_category(self, risk_level):
    if risk_level >= 0.9:
        return "🔴 CRITICAL - Pasti terdeteksi Turnitin"
    elif risk_level >= 0.7:
        return "🔴 VERY HIGH - Sangat berisiko"
    elif risk_level >= 0.5:
        return "🟠 HIGH - Berisiko tinggi"
    elif risk_level >= 0.3:
        return "🟡 MEDIUM - Berisiko sedang"
    elif risk_level >= 0.1:
        return "🟢 LOW - Probably safe"
    else:
        return "✅ VERY LOW - Safe"
```

---

## 🤖 3. AI LEVEL DETERMINATION

### 📊 Threshold untuk AI Processing:

```python
# Konfigurasi threshold
config = {
    'ai_level3_threshold': 0.7,    # Level 3: Deep restructuring
    'ai_level2_threshold': 0.5,    # Level 2: Pattern-specific
    'ai_level1_threshold': 0.3,    # Level 1: Basic AI
}

# Penentuan AI level
if risk_level >= 0.7:
    ai_level_needed = 3  # Deep AI restructuring
elif risk_level >= 0.5:
    ai_level_needed = 2  # Pattern-specific AI
elif risk_level >= 0.3:
    ai_level_needed = 1  # Basic AI enhancement
else:
    ai_level_needed = 0  # Local processing saja
```

### 🎯 AI Processing Levels:

#### 🟣 **Level 3 (Deep Restructuring)**
- Risk ≥ 70%
- Complete sentence restructuring
- Advanced synonym replacement
- Academic tone preservation
- Warna highlight: **VIOLET**

#### 🟠 **Level 2 (Pattern-Specific)**
- Risk 50-69%
- Target specific patterns
- Contextual replacements
- Moderate restructuring
- Warna highlight: **BRIGHT_GREEN**

#### 🟡 **Level 1 (Basic AI)**
- Risk 30-49%
- Basic AI enhancement
- Simple restructuring
- Synonym replacement
- Warna highlight: **YELLOW**

#### 🔵 **Local Enhanced**
- Risk < 30%
- Local processing only
- Enhanced academic replacements
- Basic synonym swapping
- Warna highlight: **TURQUOISE**

---

## 🔄 4. BALANCED HYBRID DETECTION

### 📊 Sistem Balanced Routing:

```python
def should_use_ai_balanced(self, paragraph_text, local_result, paragraph_index, total_paragraphs):
    # Target 50-50 distribution antara Local dan AI
    ai_probability = 0.5  # Base 50%
    
    # Complexity bonus
    complexity = self.calculate_paragraph_complexity(paragraph_text)
    if complexity > 0.5:
        ai_probability += 0.2
    
    # Pattern matching bonus
    pattern_matches = sum(1 for pattern in self.ai_priority_patterns 
                         if re.search(pattern, paragraph_text.lower()))
    if pattern_matches > 0:
        ai_probability += 0.15
    
    # Length bonus
    word_count = len(paragraph_text.split())
    if word_count > 50:
        ai_probability += 0.1
```

### 🧮 Complexity Calculation:

```python
def calculate_paragraph_complexity(self, text):
    words = text.split()
    sentences = text.split('.')
    
    # 5 faktor complexity:
    length_score = min(len(words) / 80, 1.0)           # 25%
    academic_density = academic_words_count / len(words) # 35%
    citation_score = min(citation_count / 2, 1.0)      # 15%
    pattern_score = matched_patterns / total_patterns   # 15%
    sentence_complexity = avg_sentence_length / 20      # 10%
    
    complexity = (
        length_score * 0.25 +
        academic_density * 0.35 +
        citation_score * 0.15 +
        pattern_score * 0.15 +
        sentence_complexity * 0.1
    )
```

---

## 📋 5. PARAGRAPH SUITABILITY CHECK

### ✅ Kriteria Paragraf Suitable:

```python
def is_paragraph_suitable_for_paraphrasing(self, text):
    # Minimum 5 kata (Enhanced) atau 15 kata (Balanced)
    word_count = len(text.split())
    if word_count < 5:  # Terlalu pendek
        return False
    
    # Skip pattern yang tidak suitable:
    unsuitable_patterns = [
        r'^\s*\d+\.\s*$',           # Hanya nomor
        r'^\s*[a-z]\.\s*$',         # Hanya huruf
        r'gambar\s+\d+',            # Caption gambar
        r'tabel\s+\d+',             # Caption tabel
        r'^\s*\([^)]+\)\s*$',       # Hanya sitasi
        r'^\s*sumber\s*:',          # Label sumber
        r'^\s*\w+\s*:\s*\w+\s*$'    # Key-value pairs
    ]
```

### ❌ Yang Tidak Diproses:

1. **Section Headers**: BAB, Chapter, dll
2. **Captions**: Gambar, Tabel, Figure
3. **Citations Only**: Referensi dalam kurung
4. **Short Phrases**: < 5 kata
5. **Tables/Lists**: Data tabular
6. **Source Labels**: "Sumber:", "Source:"

---

## 🎯 6. DECISION FLOW CHART

```
📄 Input Paragraph
       ↓
🔍 Suitability Check
       ↓
   ✅ Suitable?
       ↓
🎯 Risk Detection
   (5 categories)
       ↓
📊 Calculate Risk Score
   (0.0 - 1.0)
       ↓
🎚️ Determine AI Level
   (0, 1, 2, 3)
       ↓
🤖 Route to Processing:
   • Level 0: Local Enhanced
   • Level 1: Basic AI
   • Level 2: Pattern AI  
   • Level 3: Deep AI
       ↓
✅ Apply Changes
   with Color Coding
```

---

## 💡 7. CONTOH DETEKSI REAL

### 🔴 **HIGH RISK** (Level 3 AI):
```
"Menurut pendapat Smith (2023), sistem informasi adalah suatu kombinasi 
dari hardware, software, dan jaringan yang digunakan untuk mengumpulkan, 
memfilter, memproses, membuat, dan mendistribusikan data."
```
**Detected Patterns:**
- ✅ Academic template: "Menurut pendapat"
- ✅ Citation: "(2023)"  
- ✅ Technical definition: "sistem informasi adalah"
- ✅ Domain terms: "hardware, software, jaringan"
- **Risk Score: 0.85** → Level 3 AI

### 🟡 **MEDIUM RISK** (Level 1 AI):
```
"Penelitian ini menggunakan metode kualitatif dengan pendekatan studi kasus 
untuk menganalisis implementasi sistem di perusahaan."
```
**Detected Patterns:**
- ✅ Methodology: "metode kualitatif"
- ✅ Domain terms: "penelitian, implementasi, sistem"
- **Risk Score: 0.35** → Level 1 AI

### 🟢 **LOW RISK** (Local Only):
```
"Hasil pengujian menunjukkan bahwa aplikasi dapat berjalan dengan baik 
dan memenuhi kebutuhan pengguna sesuai dengan yang diharapkan."
```
**Detected Patterns:**
- ⚠️ Minimal patterns detected
- **Risk Score: 0.15** → Local Enhanced

---

## 🏆 Kesimpulan

Sistem deteksi menggunakan **multi-factor analysis** yang menggabungkan:

1. **Pattern Recognition** - Deteksi 5 kategori pattern berisiko
2. **Risk Scoring** - Perhitungan weighted score 0-1
3. **AI Level Routing** - Penentuan tingkat AI processing
4. **Suitability Filtering** - Filter paragraf yang tidak perlu diproses
5. **Balanced Distribution** - Distribusi 50-50 untuk perbandingan

Hasil akhir: **Intelligent routing** yang memastikan setiap paragraf mendapat treatment yang tepat sesuai tingkat risikonya!
