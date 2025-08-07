# enhanced_paraphrase_system.py
import random
import re
import json
from collections import defaultdict

class EnhancedParaphraseSystem:
    def __init__(self, synonym_file='sinonim.json'):
        print("🚀 Initializing Enhanced Paraphrase System...")
        
        # Load synonyms properly
        self.synonyms = self.load_synonyms_fixed(synonym_file)
        
        # Indonesian stopwords
        self.stopwords = {
            'yang', 'dan', 'di', 'ke', 'dari', 'dalam', 'untuk', 'pada',
            'dengan', 'adalah', 'akan', 'atau', 'juga', 'telah', 'dapat',
            'tidak', 'ada', 'ini', 'itu', 'saya', 'kami', 'kita', 'mereka',
            'sudah', 'belum', 'masih', 'sangat', 'sekali', 'lebih', 'bahwa',
            'karena', 'jika', 'maka', 'saja', 'hanya', 'bisa', 'semua'
        }
        
        # Common phrase replacements
        self.phrase_replacements = {
            'bertujuan untuk': ['dimaksudkan untuk', 'ditujukan untuk', 'bermaksud untuk'],
            'dapat': ['mampu', 'bisa', 'sanggup'],
            'menggunakan': ['memakai', 'memanfaatkan', 'mempergunakan'],
            'mengurangi': ['menurunkan', 'meminimalisir', 'menimimalisasi'],
            'tingkat': ['level', 'taraf', 'derajat'],
            'sistem': ['metode', 'cara', 'teknik', 'prosedur'],
            'pendekatan': ['metode', 'cara', 'teknik'],
            'menghasilkan': ['menciptakan', 'membuat', 'memproduksi'],
            'mempertahankan': ['menjaga', 'memelihara', 'memelihara'],
            'berbeda': ['tidak sama', 'berlainan', 'bervariasi'],
            'struktur': ['susunan', 'bentuk', 'format'],
            'pilihan': ['opsi', 'alternatif', 'seleksi']
        }
        
        print(f"✅ Loaded {len(self.synonyms)} synonym groups")
        print(f"✅ Loaded {len(self.phrase_replacements)} phrase patterns")
    
    def load_synonyms_fixed(self, filename):
        """Load synonyms with better error handling"""
        synonyms = defaultdict(list)
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            count = 0
            for word, info in data.items():
                if isinstance(info, dict) and 'sinonim' in info:
                    synonym_list = info['sinonim']
                    if isinstance(synonym_list, list) and len(synonym_list) > 0:
                        # Add main word and all synonyms
                        all_words = [word] + synonym_list
                        for w in all_words:
                            synonyms[w.lower()] = [s.lower() for s in all_words if s.lower() != w.lower()]
                        count += 1
                        
            print(f"✅ Successfully processed {count} synonym groups")
            return dict(synonyms)
            
        except Exception as e:
            print(f"❌ Error loading synonyms: {e}")
            return {}
    
    def get_synonyms(self, word):
        """Get synonyms for a word"""
        word = word.lower().strip()
        return self.synonyms.get(word, [])
    
    def phrase_replacement_strategy(self, text):
        """Replace common phrases with alternatives"""
        modified_text = text
        replacements_made = []
        
        for phrase, alternatives in self.phrase_replacements.items():
            if phrase in modified_text.lower():
                replacement = random.choice(alternatives)
                # Case-sensitive replacement
                pattern = re.compile(re.escape(phrase), re.IGNORECASE)
                if pattern.search(modified_text):
                    modified_text = pattern.sub(replacement, modified_text, count=1)
                    replacements_made.append({
                        'original': phrase,
                        'replacement': replacement
                    })
        
        return modified_text, replacements_made
    
    def word_synonym_strategy(self, text, replacement_ratio=0.4):
        """Replace individual words with synonyms"""
        words = text.split()
        modified_words = []
        replacements_made = []
        
        for word in words:
            # Clean word (remove punctuation)
            clean_word = re.sub(r'[^\w]', '', word.lower())
            
            if (clean_word not in self.stopwords and 
                len(clean_word) > 3 and 
                random.random() < replacement_ratio):
                
                synonyms = self.get_synonyms(clean_word)
                if synonyms:
                    # Choose a good synonym
                    suitable_synonyms = [
                        syn for syn in synonyms 
                        if len(syn) >= 3 and syn != clean_word
                    ]
                    
                    if suitable_synonyms:
                        chosen_synonym = random.choice(suitable_synonyms)
                        
                        # Preserve original capitalization and punctuation
                        if word[0].isupper():
                            chosen_synonym = chosen_synonym.capitalize()
                        
                        # Add back punctuation
                        punctuation = ''.join(c for c in word if not c.isalnum())
                        final_word = chosen_synonym + punctuation
                        
                        modified_words.append(final_word)
                        replacements_made.append({
                            'original': word,
                            'replacement': final_word
                        })
                    else:
                        modified_words.append(word)
                else:
                    modified_words.append(word)
            else:
                modified_words.append(word)
        
        return ' '.join(modified_words), replacements_made
    
    def sentence_restructuring_strategy(self, text):
        """Restructure sentences"""
        restructuring_patterns = [
            # Pattern replacements
            (r'\buntuk\b', 'guna'),
            (r'\boleh karena itu\b', 'maka dari itu'),
            (r'\bsehingga\b', 'yang mengakibatkan'),
            (r'\bdengan cara\b', 'melalui'),
            (r'\bdalam hal\b', 'mengenai'),
            (r'\bberdasarkan\b', 'menurut'),
            (r'\bselain itu\b', 'di samping itu'),
        ]
        
        modified_text = text
        changes_made = []
        
        for pattern, replacement in restructuring_patterns:
            if re.search(pattern, modified_text, re.IGNORECASE):
                modified_text = re.sub(pattern, replacement, modified_text, flags=re.IGNORECASE)
                changes_made.append({
                    'pattern': pattern,
                    'replacement': replacement
                })
        
        return modified_text, changes_made
    
    def calculate_similarity(self, text1, text2):
        """Calculate similarity between texts"""
        # Simple word-based similarity
        words1 = set(re.findall(r'\w+', text1.lower()))
        words2 = set(re.findall(r'\w+', text2.lower()))
        
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        if union == 0:
            return 0.0
        
        return (intersection / union) * 100
    
    def generate_paraphrase(self, text, aggressiveness=0.5):
        """Generate a single high-quality paraphrase"""
        current_text = text.strip()
        all_changes = []
        
        # Strategy 1: Phrase replacement (most effective)
        current_text, phrase_changes = self.phrase_replacement_strategy(current_text)
        all_changes.extend(phrase_changes)
        
        # Strategy 2: Word synonym replacement
        replacement_ratio = 0.3 + (aggressiveness * 0.4)  # 0.3 to 0.7
        current_text, word_changes = self.word_synonym_strategy(current_text, replacement_ratio)
        all_changes.extend(word_changes)
        
        # Strategy 3: Sentence restructuring
        if random.random() > 0.4:
            current_text, struct_changes = self.sentence_restructuring_strategy(current_text)
            all_changes.extend(struct_changes)
        
        # Calculate metrics
        similarity = self.calculate_similarity(text, current_text)
        
        return {
            'paraphrase': current_text,
            'similarity': similarity,
            'plagiarism_reduction': 100 - similarity,
            'changes_made': len(all_changes),
            'change_details': all_changes,
            'status': self.get_plagiarism_status(similarity)
        }
    
    def generate_multiple_paraphrases(self, text, num_options=3):
        """Generate multiple paraphrase options"""
        options = []
        
        # Generate options with different aggressiveness levels
        aggressiveness_levels = [0.3, 0.5, 0.7]
        
        for i in range(num_options):
            aggressiveness = aggressiveness_levels[i % len(aggressiveness_levels)]
            result = self.generate_paraphrase(text, aggressiveness)
            result['option_number'] = i + 1
            result['aggressiveness'] = aggressiveness
            options.append(result)
        
        # Sort by plagiarism reduction (best first)
        options.sort(key=lambda x: x['plagiarism_reduction'], reverse=True)
        
        return options
    
    def get_plagiarism_status(self, similarity):
        """Get plagiarism risk status"""
        if similarity >= 80:
            return "🔴 HIGH RISK - Perlu parafrase lebih lanjut"
        elif similarity >= 60:
            return "🟡 MEDIUM RISK - Cukup baik, bisa diperbaiki"
        elif similarity >= 40:
            return "🟢 LOW RISK - Parafrase baik"
        else:
            return "✅ VERY LOW RISK - Excellent paraphrase"

# Test enhanced system
if __name__ == "__main__":
    print("🧪 Testing Enhanced Paraphrase System...")
    
    # Initialize system
    paraphraser = EnhancedParaphraseSystem('sinonim.json')
    
    # Test if synonyms loaded properly
    test_words = ['menggunakan', 'penelitian', 'sistem', 'dapat']
    print(f"\n🔍 Testing synonym database:")
    for word in test_words:
        synonyms = paraphraser.get_synonyms(word)
        print(f"{word}: {synonyms[:5] if len(synonyms) > 5 else synonyms}")  # Show first 5
    
    # Test text
    test_text = "Penelitian ini bertujuan untuk mengembangkan sistem parafrase otomatis yang dapat mengurangi tingkat plagiarisme dalam dokumen akademik."
    
    print(f"\n📝 Original Text:")
    print(test_text)
    print("\n" + "="*80)
    
    # Generate paraphrases
    options = paraphraser.generate_multiple_paraphrases(test_text, num_options=3)
    
    for option in options:
        print(f"\n🔄 Paraphrase Option {option['option_number']} (Aggressiveness: {option['aggressiveness']}):")
        print(f"Text: {option['paraphrase']}")
        print(f"Similarity: {option['similarity']:.1f}%")
        print(f"Plagiarism Reduction: {option['plagiarism_reduction']:.1f}%")
        print(f"Changes Made: {option['changes_made']}")
        print(f"Status: {option['status']}")
        
        if option['change_details']:
            print("Changes:")
            for change in option['change_details'][:3]:  # Show first 3 changes
                if 'original' in change and 'replacement' in change:
                    print(f"  • {change['original']} → {change['replacement']}")
        print("-" * 60)
    
    print("\n✅ Enhanced Paraphrase System Test Complete!")
