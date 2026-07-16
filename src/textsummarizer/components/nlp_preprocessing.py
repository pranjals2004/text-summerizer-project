import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from textsummarizer.entity import NLPPreprocessingConfig
from textsummarizer.logging import logger

class NLPPreprocessing:
    def __init__(self, config: NLPPreprocessingConfig):
        self.config = config
        self._setup_nltk()

    def _setup_nltk(self):
        required_packages = ['punkt', 'punkt_tab', 'stopwords', 'averaged_perceptron_tagger', 'averaged_perceptron_tagger_eng']
        for package in required_packages:
            try:
                nltk.download(package, quiet=True)
            except Exception as e:
                logger.error(f"Failed to download NLTK package {package}: {e}")

    def count_syllables(self, word):
        word = word.lower().strip(",.!?\"'")
        if not word:
            return 0
        vowels = "aeiouy"
        count = 0
        if word[0] in vowels:
            count += 1
        for index in range(1, len(word)):
            if word[index] in vowels and word[index - 1] not in vowels:
                count += 1
        if word.endswith("e"):
            count -= 1
        if count == 0:
            count = 1
        return count

    def calculate_readability(self, text, word_count, sent_count):
        if word_count == 0 or sent_count == 0:
            return 100.0, "Very Easy"
        
        words = re.findall(r'\b\w+\b', text.lower())
        total_syllables = sum(self.count_syllables(w) for w in words)
        
        score = 206.835 - 1.015 * (word_count / sent_count) - 84.6 * (total_syllables / word_count)
        score = max(0.0, min(100.0, score))
        
        if score >= 90:
            grade = "Very Easy (5th Grade)"
        elif score >= 80:
            grade = "Easy (6th Grade)"
        elif score >= 70:
            grade = "Fairly Easy (7th Grade)"
        elif score >= 60:
            grade = "Standard (8th-9th Grade)"
        elif score >= 50:
            grade = "Fairly Difficult (10th-12th Grade)"
        elif score >= 30:
            grade = "Difficult (College)"
        else:
            grade = "Very Difficult (College Graduate)"
            
        return round(score, 1), grade

    def map_pos_tag(self, tag):
        if tag.startswith('NN'):
            return 'Nouns'
        elif tag.startswith('VB'):
            return 'Verbs'
        elif tag.startswith('JJ'):
            return 'Adjectives'
        elif tag.startswith('RB'):
            return 'Adverbs'
        elif tag.startswith('PRP') or tag == 'WP':
            return 'Pronouns'
        elif tag in ['CC']:
            return 'Conjunctions'
        elif tag in ['IN', 'TO']:
            return 'Prepositions'
        elif tag in ['DT', 'PDT', 'WDT']:
            return 'Determiners'
        else:
            return 'Others'

    def preprocess_text(self, text):
        if not text or not text.strip():
            return {
                "char_count": 0, "word_count": 0, "sentence_count": 0,
                "lexical_diversity": 0.0, "readability_score": 100.0, "readability_grade": "N/A",
                "pos_distribution": {}, "word_frequencies": [], "filtered_tokens": []
            }
            
        char_count = len(text)
        sentences = sent_tokenize(text)
        sentence_count = len(sentences)
        
        words = word_tokenize(text)
        clean_words = [w.lower() for w in words if w.isalnum()]
        word_count = len(clean_words)
        
        unique_words = set(clean_words)
        lexical_diversity = round((len(unique_words) / word_count) * 100, 1) if word_count > 0 else 0.0
        
        readability_score, readability_grade = self.calculate_readability(text, word_count, sentence_count)
        
        try:
            stop_words = set(stopwords.words('english'))
        except Exception:
            stop_words = set()
        filtered_tokens = [w for w in clean_words if w not in stop_words]
        
        freq_dict = {}
        for w in filtered_tokens:
            freq_dict[w] = freq_dict.get(w, 0) + 1
        
        sorted_freqs = sorted(freq_dict.items(), key=lambda x: x[1], reverse=True)[:15]
        word_frequencies = [{"word": word, "count": count} for word, count in sorted_freqs]
        
        pos_distribution = {
            "Nouns": 0, "Verbs": 0, "Adjectives": 0, "Adverbs": 0,
            "Pronouns": 0, "Conjunctions": 0, "Prepositions": 0, "Determiners": 0, "Others": 0
        }
        try:
            tagged_words = nltk.pos_tag(words)
            for _, tag in tagged_words:
                category = self.map_pos_tag(tag)
                pos_distribution[category] += 1
        except Exception as e:
            logger.error(f"Error in POS Tagging: {e}")
            
        return {
            "char_count": char_count,
            "word_count": word_count,
            "sentence_count": sentence_count,
            "lexical_diversity": lexical_diversity,
            "readability_score": readability_score,
            "readability_grade": readability_grade,
            "pos_distribution": pos_distribution,
            "word_frequencies": word_frequencies,
            "filtered_tokens": filtered_tokens[:100]
        }

    def get_local_extractive_summary(self, text, num_sentences=3):
        if not text:
            return ""
        sentences = sent_tokenize(text)
        if len(sentences) <= num_sentences:
            return text
            
        words = word_tokenize(text.lower())
        clean_words = [w for w in words if w.isalnum()]
        try:
            stop_words = set(stopwords.words('english'))
        except Exception:
            stop_words = set()
            
        freq_dict = {}
        for w in clean_words:
            if w not in stop_words:
                freq_dict[w] = freq_dict.get(w, 0) + 1
                
        if not freq_dict:
            return " ".join(sentences[:num_sentences])
            
        sent_scores = {}
        for i, sent in enumerate(sentences):
            score = 0
            sent_words = word_tokenize(sent.lower())
            for w in sent_words:
                if w in freq_dict:
                    score += freq_dict[w]
            sent_scores[i] = score / (len(sent_words) + 1)
            
        top_indices = sorted(sent_scores, key=sent_scores.get, reverse=True)[:num_sentences]
        top_indices.sort()
        
        return " ".join([sentences[i] for i in top_indices])
