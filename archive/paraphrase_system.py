# paraphrase_system.py
import random
import re
from improved_indonesian_stemmer import ImprovedIndonesianStemmer
from collections import defaultdict
import json

class IndonesianParaphraseSystem:
    def __init__(self, synonym_file='sinonim.json'):
        print("🚀 Initializing Paraphrase System...")
        
        # Load stemmer with synonyms
        self.stemmer = ImprovedIndonesianStemmer(synonym_file)
        
        # Paraphrasing strategies
        self.strategies = [
            'synonym_replacement',
            'sentence_restructuring', 
            'active_passive_conversion',
            'word_order_variation',
            'synonym_clustering'
        ]
        
        # Indonesian sentence patterns
        self.sentence_patterns = {
            'active_to_passive': {
                'indicators': ['me', 'men', 'mem', 'meng'],
                'transformation': 'di-'
            },
            'passive_to_active': {
                'indicators': ['di'],
                'transformation': 'me-'
            }
        }
        
        print(f"✅ Loaded {len(self.stemmer.synonyms)} synonym groups")
    
    def calculate_similarity(self, text1, text2):
        """Calculate similarity between two texts"""
        # Process both texts
        processed1 = set(self.stemmer.process_text(text1).split())
        processed2 = set(self.stemmer.process_text(text2).split())
        
        # Calculate Jaccard similarity
        intersection = len(processed1.intersection(processed2))
        union = len(processed1.union(processed2))
        
        if union == 0:
            return 0.0
        
        similarity = intersection / union
        return similarity * 100  # Return as percentage
    
    def synonym_replacement_strategy(self, text, replacement_ratio=0.4):
        """Replace words with synonyms"""
        words = text.split()
        modified_words = []
        replacements_made = []
        
        for word in words:
            original_word = word.lower().strip('.,!?;:')
            synonyms = self.stemmer.get_synonyms(original_word)
            
            # Replace with probability
            if synonyms and random.random() < replacement_ratio:
                # Choose best synonym (not too different in length)
                suitable_synonyms = [
                    syn for syn in synonyms 
                    if abs(len(syn) - len(original_word)) <= 3
                ]
                
                if suitable_synonyms:
                    chosen_synonym = random.choice(suitable_synonyms)
                    modified_words.append(chosen_synonym)
                    replacements_made.append({
                        'original': original_word,
                        'replacement': chosen_synonym,
                        'position': len(modified_words) - 1
                    })
                else:
                    modified_words.append(word)
            else:
                modified_words.append(word)
        
        return ' '.join(modified_words), replacements_made
    
    def sentence_restructuring_strategy(self, text):
        """Restructure sentence patterns"""
        # Simple restructuring patterns
        restructuring_patterns = [
            # "A adalah B" -> "B merupakan A"
            (r'(\w+)\s+adalah\s+(\w+)', r'\2 merupakan \1'),
            
            # "untuk X" -> "guna X" 
            (r'\buntuk\b', 'guna'),
            
            # "dengan cara" -> "melalui"
            (r'dengan cara', 'melalui'),
            
            # "sehingga" -> "yang mengakibatkan"
            (r'\bsehingga\b', 'yang mengakibatkan'),
            
            # "oleh karena itu" -> "maka dari itu"
            (r'oleh karena itu', 'maka dari itu'),
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
    
    def word_order_variation(self, text):
        """Vary word order while maintaining meaning"""
        sentences = text.split('.')
        modified_sentences = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            
            # Simple word order variations
            words = sentence.split()
            
            if len(words) > 4:
                # Try to move adjectives or adverbs
                modified_words = words.copy()
                
                # Find adjective patterns and move them
                for i, word in enumerate(words):
                    if word.lower() in ['sangat', 'lebih', 'paling', 'cukup', 'agak']:
                        if i < len(words) - 1:
                            # Move intensifier closer to the word it modifies
                            target_word = words[i + 1]
                            modified_words[i] = target_word
                            modified_words[i + 1] = word
                            break
                
                modified_sentences.append(' '.join(modified_words))
            else:
                modified_sentences.append(sentence)
        
        return '. '.join(modified_sentences)
    
    def generate_paraphrase_options(self, text, num_options=3):
        """Generate multiple paraphrase options"""
        options = []
        
        for i in range(num_options):
            # Combine different strategies
            current_text = text
            strategies_used = []
            
            # Strategy 1: Synonym replacement
            if random.random() > 0.3:
                current_text, replacements = self.synonym_replacement_strategy(
                    current_text, 
                    replacement_ratio=random.uniform(0.2, 0.6)
                )
                if replacements:
                    strategies_used.append('synonym_replacement')
            
            # Strategy 2: Sentence restructuring  
            if random.random() > 0.5:
                current_text, changes = self.sentence_restructuring_strategy(current_text)
                if changes:
                    strategies_used.append('sentence_restructuring')
            
            # Strategy 3: Word order variation
            if random.random() > 0.6:
                current_text = self.word_order_variation(current_text)
                strategies_used.append('word_order_variation')
            
            # Calculate similarity with original
            similarity = self.calculate_similarity(text, current_text)
            
            options.append({
                'paraphrase': current_text,
                'similarity_to_original': similarity,
                'strategies_used': strategies_used,
                'quality_score': self.calculate_quality_score(text, current_text)
            })
        
        # Sort by quality score
        options.sort(key=lambda x: x['quality_score'], reverse=True)
        return options
    
    def calculate_quality_score(self, original, paraphrase):
        """Calculate quality score for paraphrase"""
        # Factors: diversity, readability, length preservation
        similarity = self.calculate_similarity(original, paraphrase)
        
        # Ideal similarity: 40-70% (enough change but preserves meaning)
        if 40 <= similarity <= 70:
            similarity_score = 100
        elif similarity > 70:
            similarity_score = 100 - (similarity - 70) * 2  # Penalty for too similar
        else:
            similarity_score = similarity * 2  # Penalty for too different
        
        # Length preservation score
        len_ratio = len(paraphrase) / len(original) if len(original) > 0 else 0
        if 0.8 <= len_ratio <= 1.2:
            length_score = 100
        else:
            length_score = max(0, 100 - abs(len_ratio - 1) * 100)
        
        # Word diversity score
        original_words = set(original.lower().split())
        paraphrase_words = set(paraphrase.lower().split())
        diversity = len(paraphrase_words - original_words) / len(original_words) if original_words else 0
        diversity_score = min(100, diversity * 200)
        
        # Weighted final score
        quality_score = (
            similarity_score * 0.4 + 
            length_score * 0.3 + 
            diversity_score * 0.3
        )
        
        return round(quality_score, 2)
    
    def analyze_plagiarism_reduction(self, original, paraphrase):
        """Analyze how much plagiarism was reduced"""
        original_similarity = 100  # Original is 100% similar to itself
        paraphrase_similarity = self.calculate_similarity(original, paraphrase)
        
        reduction_percentage = original_similarity - paraphrase_similarity
        
        return {
            'original_similarity': original_similarity,
            'paraphrase_similarity': paraphrase_similarity,
            'plagiarism_reduction': reduction_percentage,
            'status': self.get_plagiarism_status(paraphrase_similarity)
        }
    
    def get_plagiarism_status(self, similarity):
        """Get plagiarism status based on similarity"""
        if similarity >= 80:
            return "HIGH RISK - Perlu parafrase lebih lanjut"
        elif similarity >= 50:
            return "MEDIUM RISK - Cukup baik, bisa diperbaiki"
        elif similarity >= 30:
            return "LOW RISK - Parafrase baik"
        else:
            return "VERY LOW RISK - Excellent paraphrase"

# Test system
if __name__ == "__main__":
    print("🧪 Testing Complete Paraphrase System...")
    
    # Initialize system
    paraphraser = IndonesianParaphraseSystem('sinonim.json')
    
    # Test text
    test_text = """Penelitian ini bertujuan untuk mengembangkan sistem parafrase otomatis 
    yang dapat mengurangi tingkat plagiarisme dalam dokumen akademik. Sistem menggunakan 
    pendekatan berbasis aturan dan sinonim untuk menghasilkan variasi kalimat yang 
    mempertahankan makna asli tetapi berbeda dalam struktur dan pilihan kata."""
    
    print(f"\n📝 Original Text:")
    print(test_text)
    print("\n" + "="*80)
    
    # Generate paraphrase options
    options = paraphraser.generate_paraphrase_options(test_text, num_options=3)
    
    for i, option in enumerate(options, 1):
        print(f"\n🔄 Paraphrase Option {i}:")
        print(f"Text: {option['paraphrase']}")
        print(f"Quality Score: {option['quality_score']}")
        print(f"Similarity to Original: {option['similarity_to_original']:.2f}%")
        print(f"Strategies Used: {', '.join(option['strategies_used'])}")
        
        # Analyze plagiarism reduction
        analysis = paraphraser.analyze_plagiarism_reduction(test_text, option['paraphrase'])
        print(f"Plagiarism Reduction: {analysis['plagiarism_reduction']:.2f}%")
        print(f"Status: {analysis['status']}")
        print("-" * 60)
    
    print("\n✅ Paraphrase System Test Complete!")
