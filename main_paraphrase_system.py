# main_paraphrase_system.py
"""
Sistem Parafrase Anti-Plagiarisme Bahasa Indonesia
File Utama - All-in-One Solution
Author: DevNoLife
Version: 1.0
"""

import json
import random
import re
import os
from collections import defaultdict
from datetime import datetime

class IndonesianParaphraseSystem:
    def __init__(self, synonym_file=None):
        print("🚀 Initializing Indonesian Paraphrase System...")
        
        # Load synonyms
        self.synonyms = self.load_synonyms(synonym_file) if synonym_file else {}
        
        # Indonesian stopwords
        self.stopwords = {
            'yang', 'dan', 'di', 'ke', 'dari', 'dalam', 'untuk', 'pada',
            'dengan', 'adalah', 'akan', 'atau', 'juga', 'telah', 'dapat',
            'tidak', 'ada', 'ini', 'itu', 'saya', 'kami', 'kita', 'mereka',
            'sudah', 'belum', 'masih', 'sangat', 'sekali', 'lebih', 'bahwa',
            'karena', 'jika', 'maka', 'saja', 'hanya', 'bisa', 'semua', 'akan'
        }
        
        # Enhanced phrase replacements for Indonesian academic text
        self.phrase_replacements = {
            # Academic phrases
            'bertujuan untuk': ['dimaksudkan untuk', 'ditujukan untuk', 'bermaksud untuk', 'berupaya untuk'],
            'penelitian ini': ['studi ini', 'kajian ini', 'riset ini', 'investigasi ini'],
            'hasil penelitian': ['temuan riset', 'output kajian', 'hasil studi', 'temuan penelitian'],
            'dapat': ['mampu', 'bisa', 'sanggup', 'dapat'],
            'menggunakan': ['memakai', 'memanfaatkan', 'mempergunakan', 'mengaplikasikan'],
            'menunjukkan': ['memperlihatkan', 'mengindikasikan', 'mendemonstrasikan', 'membuktikan'],
            'mengurangi': ['menurunkan', 'meminimalisir', 'menimimalisasi', 'memperkecil'],
            'meningkatkan': ['menaikkan', 'memperbesar', 'mengoptimalkan', 'memaksimalkan'],
            'tingkat': ['level', 'taraf', 'derajat', 'kadar'],
            'sistem': ['metode', 'cara', 'teknik', 'prosedur', 'mekanisme'],
            'pendekatan': ['metode', 'cara', 'teknik', 'strategi'],
            'menghasilkan': ['menciptakan', 'membuat', 'memproduksi', 'melahirkan'],
            'mempertahankan': ['menjaga', 'memelihara', 'mempertahan', 'melestarikan'],
            'berbeda': ['tidak sama', 'berlainan', 'bervariasi', 'beragam'],
            'struktur': ['susunan', 'bentuk', 'format', 'konstruksi'],
            'pilihan': ['opsi', 'alternatif', 'seleksi', 'variasi'],
            'dokumen': ['naskah', 'berkas', 'file', 'manuscript'],
            'akademik': ['ilmiah', 'pendidikan', 'universitas', 'kampus'],
            'otomatis': ['automatik', 'mandiri', 'sendiri', 'auto'],
            
            # Connective phrases
            'oleh karena itu': ['maka dari itu', 'dengan demikian', 'karena hal tersebut', 'akibatnya'],
            'selain itu': ['di samping itu', 'tambahan pula', 'lebih lanjut', 'furthermore'],
            'berdasarkan': ['menurut', 'berlandaskan', 'atas dasar', 'sesuai dengan'],
            'sehingga': ['yang mengakibatkan', 'sampai', 'hingga', 'alhasil'],
            'dengan cara': ['melalui', 'lewat', 'via', 'menggunakan cara'],
            'dalam hal': ['mengenai', 'terkait', 'berkaitan dengan', 'perihal'],
            'untuk': ['guna', 'bagi', 'demi', 'agar'],
            
            # Time and sequence
            'kemudian': ['selanjutnya', 'setelah itu', 'berikutnya', 'lalu'],
            'sebelumnya': ['terdahulu', 'sebelum ini', 'lebih dulu', 'dahulu'],
            'saat ini': ['sekarang', 'dewasa ini', 'kini', 'pada masa ini'],
            'pada akhirnya': ['akhirnya', 'kesimpulannya', 'pada ujungnya', 'hasilnya'],
        }
        
        # Sentence restructuring patterns
        self.restructuring_patterns = [
            # Convert active to passive patterns
            (r'(\w+)\s+menggunakan\s+(\w+)', r'\2 digunakan oleh \1'),
            (r'(\w+)\s+mengembangkan\s+(\w+)', r'\2 dikembangkan oleh \1'),
            (r'(\w+)\s+menganalisis\s+(\w+)', r'\2 dianalisis oleh \1'),
            
            # Reorder sentence components
            (r'^([A-Z]\w+)\s+ini\s+([a-z]\w+)', r'Pada \1 ini, \2'),
            (r'sangat\s+(\w+)', r'\1 sekali'),
            (r'lebih\s+(\w+)', r'\1 yang lebih'),
        ]
        
        print(f"✅ Loaded {len(self.synonyms)} synonym entries")
        print(f"✅ Loaded {len(self.phrase_replacements)} phrase patterns")
        print("✅ System ready for paraphrasing!")
    
    def load_synonyms(self, filename):
        """Load synonym database from JSON file"""
        if not filename or not os.path.exists(filename):
            print("⚠️  No synonym file provided or file not found")
            return {}
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            synonyms = defaultdict(list)
            count = 0
            
            for word, info in data.items():
                if isinstance(info, dict) and 'sinonim' in info:
                    synonym_list = info['sinonim']
                    if isinstance(synonym_list, list) and len(synonym_list) > 0:
                        # Add bidirectional synonyms
                        all_words = [word] + synonym_list
                        for w in all_words:
                            clean_w = w.lower().strip()
                            synonyms[clean_w] = [s.lower().strip() for s in all_words if s.lower().strip() != clean_w]
                        count += 1
            
            print(f"✅ Successfully loaded {count} synonym groups from {filename}")
            return dict(synonyms)
            
        except Exception as e:
            print(f"❌ Error loading synonyms: {e}")
            return {}
    
    def get_synonyms(self, word):
        """Get synonyms for a word"""
        return self.synonyms.get(word.lower().strip(), [])
    
    def calculate_similarity(self, text1, text2):
        """Calculate similarity percentage between two texts"""
        # Tokenize and clean
        words1 = set(re.findall(r'\w+', text1.lower()))
        words2 = set(re.findall(r'\w+', text2.lower()))
        
        if not words1 and not words2:
            return 100.0
        if not words1 or not words2:
            return 0.0
        
        # Calculate Jaccard similarity
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        return (intersection / union) * 100 if union > 0 else 0.0
    
    def phrase_replacement_strategy(self, text):
        """Replace phrases with alternatives"""
        modified_text = text
        replacements_made = []
        
        # Sort phrases by length (longer first) to avoid partial replacements
        sorted_phrases = sorted(self.phrase_replacements.items(), key=lambda x: len(x[0]), reverse=True)
        
        for phrase, alternatives in sorted_phrases:
            # Case-insensitive search
            pattern = re.compile(re.escape(phrase), re.IGNORECASE)
            match = pattern.search(modified_text)
            
            if match:
                replacement = random.choice(alternatives)
                # Preserve original case
                if match.group().istitle():
                    replacement = replacement.capitalize()
                elif match.group().isupper():
                    replacement = replacement.upper()
                
                modified_text = pattern.sub(replacement, modified_text, count=1)
                replacements_made.append({
                    'original': phrase,
                    'replacement': replacement,
                    'position': match.start()
                })
        
        return modified_text, replacements_made
    
    def word_synonym_strategy(self, text, replacement_ratio=0.4):
        """Replace individual words with synonyms"""
        words = re.findall(r'\b\w+\b|\W+', text)  # Keep punctuation
        modified_words = []
        replacements_made = []
        
        for i, word in enumerate(words):
            if re.match(r'\w+', word):  # It's a word
                clean_word = word.lower()
                
                if (clean_word not in self.stopwords and 
                    len(clean_word) > 3 and 
                    random.random() < replacement_ratio):
                    
                    synonyms = self.get_synonyms(clean_word)
                    if synonyms:
                        # Filter suitable synonyms
                        suitable_synonyms = [
                            syn for syn in synonyms 
                            if len(syn) >= 3 and syn != clean_word
                        ]
                        
                        if suitable_synonyms:
                            chosen_synonym = random.choice(suitable_synonyms)
                            
                            # Preserve case
                            if word.istitle():
                                chosen_synonym = chosen_synonym.capitalize()
                            elif word.isupper():
                                chosen_synonym = chosen_synonym.upper()
                            
                            modified_words.append(chosen_synonym)
                            replacements_made.append({
                                'original': word,
                                'replacement': chosen_synonym,
                                'position': i
                            })
                        else:
                            modified_words.append(word)
                    else:
                        modified_words.append(word)
                else:
                    modified_words.append(word)
            else:
                modified_words.append(word)
        
        return ''.join(modified_words), replacements_made
    
    def sentence_restructuring_strategy(self, text):
        """Apply sentence restructuring patterns"""
        modified_text = text
        changes_made = []
        
        for pattern, replacement in self.restructuring_patterns:
            if re.search(pattern, modified_text, re.IGNORECASE):
                old_text = modified_text
                modified_text = re.sub(pattern, replacement, modified_text, flags=re.IGNORECASE)
                if old_text != modified_text:
                    changes_made.append({
                        'pattern': pattern,
                        'replacement': replacement
                    })
        
        return modified_text, changes_made
    
    def generate_paraphrase(self, text, aggressiveness=0.5):
        """Generate a single paraphrase with specified aggressiveness"""
        if not text or not text.strip():
            return {
                'paraphrase': '',
                'similarity': 100.0,
                'plagiarism_reduction': 0.0,
                'changes_made': 0,
                'change_details': [],
                'status': '❌ No text provided'
            }
        
        current_text = text.strip()
        all_changes = []
        
        # Enhanced strategy selection based on text characteristics
        text_length = len(current_text.split())
        is_academic_text = self.is_academic_text(current_text)
        
        # Strategy 1: Phrase replacement (most effective)
        current_text, phrase_changes = self.phrase_replacement_strategy(current_text)
        all_changes.extend(phrase_changes)
        
        # Strategy 2: Word synonym replacement with adaptive ratio
        if is_academic_text:
            replacement_ratio = min(0.3 + (aggressiveness * 0.4), 0.8)  # More aggressive for academic text
        else:
            replacement_ratio = min(0.2 + (aggressiveness * 0.5), 0.7)  # Standard ratio
            
        current_text, word_changes = self.word_synonym_strategy(current_text, replacement_ratio)
        all_changes.extend(word_changes)
        
        # Strategy 3: Sentence restructuring (for longer texts and higher aggressiveness)
        if text_length > 50 and aggressiveness > 0.4 and random.random() > 0.3:
            current_text, struct_changes = self.sentence_restructuring_strategy(current_text)
            all_changes.extend(struct_changes)
        
        # Strategy 4: Academic-specific paraphrasing
        if is_academic_text and aggressiveness > 0.5:
            current_text, academic_changes = self.academic_paraphrasing_strategy(current_text)
            all_changes.extend(academic_changes)
        
        # Calculate metrics
        similarity = self.calculate_similarity(text, current_text)
        plagiarism_reduction = 100 - similarity
        
        return {
            'paraphrase': current_text,
            'similarity': round(similarity, 2),
            'plagiarism_reduction': round(plagiarism_reduction, 2),
            'changes_made': len(all_changes),
            'change_details': all_changes,
            'status': self._get_plagiarism_status(similarity),
            'text_type': 'academic' if is_academic_text else 'general',
            'original_length': text_length,
            'paraphrase_length': len(current_text.split())
        }
    
    def generate_multiple_paraphrases(self, text, num_options=3):
        """Generate multiple paraphrase options"""
        if not text or not text.strip():
            return []
        
        options = []
        aggressiveness_levels = [0.3, 0.5, 0.7, 0.4, 0.6]  # Different levels
        
        for i in range(num_options):
            aggressiveness = aggressiveness_levels[i % len(aggressiveness_levels)]
            
            result = self.generate_paraphrase(text, aggressiveness)
            result['option_number'] = i + 1
            result['aggressiveness'] = aggressiveness
            options.append(result)
        
        # Sort by plagiarism reduction (best first)
        options.sort(key=lambda x: x['plagiarism_reduction'], reverse=True)
        
        # Re-number after sorting
        for i, option in enumerate(options):
            option['option_number'] = i + 1
        
        return options
    
    def analyze_plagiarism(self, original_text, paraphrased_text):
        """Analyze plagiarism between original and paraphrased text"""
        similarity = self.calculate_similarity(original_text, paraphrased_text)
        
        return {
            'similarity_percentage': round(similarity, 2),
            'plagiarism_reduction': round(100 - similarity, 2),
            'status': self._get_plagiarism_status(similarity),
            'recommendation': self._get_recommendation(similarity)
        }
    
    def _get_plagiarism_status(self, similarity):
        """Get plagiarism risk status based on similarity"""
        if similarity >= 80:
            return "🔴 HIGH RISK - Perlu parafrase lebih lanjut"
        elif similarity >= 60:
            return "🟡 MEDIUM RISK - Cukup baik, bisa diperbaiki"
        elif similarity >= 40:
            return "🟢 LOW RISK - Parafrase baik"
        else:
            return "✅ VERY LOW RISK - Excellent paraphrase"
    
    def _get_recommendation(self, similarity):
        """Get recommendation based on similarity score"""
        if similarity >= 80:
            return "Tingkatkan aggressiveness parafrase atau coba strategi yang berbeda"
        elif similarity >= 60:
            return "Parafrase sudah baik, tambahkan beberapa perubahan lagi"
        elif similarity >= 40:
            return "Parafrase berkualitas baik dan aman untuk digunakan"
        else:
            return "Parafrase excellent! Tingkat plagiarisme sangat rendah"
    
    def batch_paraphrase(self, text_list, aggressiveness=0.5):
        """Process multiple texts at once"""
        results = []
        
        for i, text in enumerate(text_list):
            result = self.generate_paraphrase(text, aggressiveness)
            result['batch_number'] = i + 1
            results.append(result)
        
        return results
    
    def is_academic_text(self, text):
        """Detect if text is academic/formal writing"""
        academic_indicators = [
            'penelitian', 'menurut', 'berdasarkan', 'hasil', 'analisis',
            'teori', 'konsep', 'definisi', 'metode', 'pendekatan',
            'sistem', 'implementasi', 'evaluasi', 'kajian', 'studi',
            'universitas', 'jurnal', 'referensi', 'pustaka', 'akademik'
        ]
        
        text_lower = text.lower()
        indicator_count = sum(1 for indicator in academic_indicators if indicator in text_lower)
        
        # If 3+ academic indicators in text, consider it academic
        return indicator_count >= 3
    
    def academic_paraphrasing_strategy(self, text):
        """Specialized paraphrasing for academic text"""
        academic_replacements = {
            # Research terminology
            'penelitian ini menunjukkan': ['studi ini mengindikasikan', 'riset ini memperlihatkan', 'kajian ini mendemonstrasikan'],
            'hasil penelitian': ['temuan riset', 'output studi', 'hasil kajian', 'temuan investigasi'],
            'metode penelitian': ['metodologi riset', 'pendekatan penelitian', 'teknik investigasi'],
            'tujuan penelitian': ['objektif studi', 'sasaran riset', 'target kajian'],
            
            # Academic verbs
            'menganalisis': ['mengkaji', 'menelaah', 'menginvestigasi', 'mengeksplorasi'],
            'mengidentifikasi': ['mengenali', 'menemukan', 'mendeteksi', 'melacak'],
            'mengembangkan': ['membangun', 'menciptakan', 'merancang', 'menyusun'],
            'mengevaluasi': ['menilai', 'mengukur', 'menaksir', 'menganalisis'],
            
            # Formal transitions
            'dengan demikian': ['oleh karena itu', 'maka dari itu', 'akibatnya', 'konsekuensinya'],
            'selanjutnya': ['berikutnya', 'kemudian', 'setelah itu', 'tahap selanjutnya'],
            'sebagai tambahan': ['lebih lanjut', 'di samping itu', 'selain itu', 'furthermore'],
            
            # Technical terms
            'signifikan': ['bermakna', 'berarti', 'substansial', 'penting'],
            'optimal': ['terbaik', 'maksimal', 'ideal', 'efektif'],
            'efisien': ['produktif', 'ekonomis', 'hemat', 'streamlined'],
        }
        
        modified_text = text
        changes_made = []
        
        for phrase, alternatives in academic_replacements.items():
            if phrase in modified_text.lower():
                replacement = random.choice(alternatives)
                pattern = re.compile(re.escape(phrase), re.IGNORECASE)
                if pattern.search(modified_text):
                    modified_text = pattern.sub(replacement, modified_text, count=1)
                    changes_made.append({
                        'type': 'academic_phrase',
                        'original': phrase,
                        'replacement': replacement
                    })
        
        return modified_text, changes_made
    
    def enhanced_similarity_calculation(self, text1, text2):
        """Enhanced similarity calculation considering semantic meaning"""
        # Basic word-based similarity
        basic_similarity = self.calculate_similarity(text1, text2)
        
        # Semantic similarity based on key concepts
        concepts1 = self.extract_key_concepts(text1)
        concepts2 = self.extract_key_concepts(text2)
        
        if concepts1 and concepts2:
            concept_overlap = len(concepts1.intersection(concepts2)) / len(concepts1.union(concepts2))
            semantic_similarity = concept_overlap * 100
            
            # Weight: 70% basic similarity, 30% semantic similarity
            combined_similarity = (basic_similarity * 0.7) + (semantic_similarity * 0.3)
            return combined_similarity
        
        return basic_similarity
    
    def extract_key_concepts(self, text):
        """Extract key concepts from text for semantic analysis"""
        # Remove stopwords and extract meaningful terms
        words = re.findall(r'\w+', text.lower())
        meaningful_words = [
            word for word in words 
            if (word not in self.stopwords and 
                len(word) > 4 and 
                word.isalpha())
        ]
        
        return set(meaningful_words)
    
    def calculate_text_complexity(self, text):
        """Calculate text complexity score"""
        sentences = text.split('.')
        words = text.split()
        
        # Average sentence length
        avg_sentence_length = len(words) / len(sentences) if sentences else 0
        
        # Academic vocabulary density
        academic_words = ['penelitian', 'analisis', 'metode', 'sistem', 'implementasi', 'evaluasi']
        academic_density = sum(1 for word in words if word.lower() in academic_words) / len(words) if words else 0
        
        # Complexity score (0-100)
        complexity = min((avg_sentence_length / 20) * 50 + (academic_density * 50), 100)
        
        return complexity


def main():
    """Main function untuk testing sistem"""
    print("=" * 80)
    print("🎯 SISTEM PARAFRASE ANTI-PLAGIARISME BAHASA INDONESIA")
    print("=" * 80)
    
    # Initialize system
    paraphraser = IndonesianParaphraseSystem('sinonim.json')
    
    print("\n📝 DEMO PENGGUNAAN SISTEM:")
    print("-" * 50)
    
    # Test text
    test_text = """Penelitian ini bertujuan untuk mengembangkan sistem parafrase otomatis yang dapat mengurangi tingkat plagiarisme dalam dokumen akademik. Sistem menggunakan pendekatan berbasis aturan dan sinonim untuk menghasilkan variasi kalimat yang mempertahankan makna asli tetapi berbeda dalam struktur dan pilihan kata."""
    
    print(f"TEKS ASLI:")
    print(f"'{test_text}'")
    print("\n" + "=" * 80)
    
    # Generate multiple paraphrases
    options = paraphraser.generate_multiple_paraphrases(test_text, num_options=3)
    
    for option in options:
        print(f"\n🔄 PARAFRASE #{option['option_number']} (Aggressiveness: {option['aggressiveness']}):")
        print(f"HASIL: '{option['paraphrase']}'")
        print(f"📊 STATISTIK:")
        print(f"   • Similarity: {option['similarity']}%")
        print(f"   • Plagiarism Reduction: {option['plagiarism_reduction']}%") 
        print(f"   • Changes Made: {option['changes_made']}")
        print(f"   • Status: {option['status']}")
        
        if option['change_details']:
            print(f"📝 PERUBAHAN YANG DILAKUKAN:")
            for j, change in enumerate(option['change_details'][:5], 1):  # Show max 5 changes
                if 'original' in change and 'replacement' in change:
                    print(f"   {j}. '{change['original']}' → '{change['replacement']}'")
        print("-" * 80)
    
    # Demo analysis
    best_paraphrase = options[0]['paraphrase']
    analysis = paraphraser.analyze_plagiarism(test_text, best_paraphrase)
    
    print(f"\n🔍 ANALISIS PLAGIARISME:")
    print(f"   • Similarity: {analysis['similarity_percentage']}%")
    print(f"   • Reduction: {analysis['plagiarism_reduction']}%")
    print(f"   • Status: {analysis['status']}")
    print(f"   • Rekomendasi: {analysis['recommendation']}")
    
    print("\n✅ DEMO SELESAI!")
    print("=" * 80)


if __name__ == "__main__":
    main()
