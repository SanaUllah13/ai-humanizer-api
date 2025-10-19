import ssl
import random
import warnings

import nltk
import spacy
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
from sentence_transformers import SentenceTransformer, util

warnings.filterwarnings("ignore", category=FutureWarning)

NLP_GLOBAL = spacy.load("en_core_web_sm")

def download_nltk_resources():
    """
    Download required NLTK resources if not already installed.
    """
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context

    resources = ['punkt', 'averaged_perceptron_tagger', 'punkt_tab','wordnet','averaged_perceptron_tagger_eng']
    for resource in resources:
        try:
            nltk.download(resource, quiet=True)
        except Exception as e:
            print(f"Error downloading {resource}: {str(e)}")


# This class  contains methods to humanize academic text, such as improving readability or
# simplifying complex language.
class AcademicTextHumanizer:
    """
    Transforms text into a more formal (academic) style:
      - Expands contractions
      - Adds academic transitions
      - Optionally converts some sentences to passive voice
      - Optionally replaces words with synonyms for more formality
    """

    def __init__(
        self,
        model_name='paraphrase-MiniLM-L6-v2',
        p_passive=0.2,
        p_synonym_replacement=0.3,
        p_academic_transition=0.3,
        seed=None
    ):
        if seed is not None:
            random.seed(seed)

        self.nlp = spacy.load("en_core_web_sm")
        self.model = SentenceTransformer(model_name)

        # Transformation probabilities
        self.p_passive = p_passive
        self.p_synonym_replacement = p_synonym_replacement
        self.p_academic_transition = p_academic_transition

        # Common academic and natural transitions
        self.academic_transitions = [
            "Moreover,", "Additionally,", "Furthermore,", "Hence,", 
            "Therefore,", "Consequently,", "Nonetheless,", "Nevertheless,",
            "Subsequently,", "Indeed,", "In fact,", "Notably,", "Clearly,",
            "Evidently,", "Undoubtedly,", "However,", "Meanwhile,"
        ]

    def humanize_text(self, text, use_passive=False, use_synonyms=False):
        import re
        
        # 1. Expand contractions FIRST, before any tokenization
        text = self.expand_contractions(text)
        
        doc = self.nlp(text)
        transformed_sentences = []

        for i, sent in enumerate(doc.sents):
            sentence_str = sent.text.strip()

            # 2. Optionally replace words with synonyms first
            if use_synonyms and random.random() < self.p_synonym_replacement:
                sentence_str = self.replace_with_synonyms(sentence_str)
            
            # 3. Add academic transitions (only to some sentences, not the first)
            if i > 0 and random.random() < self.p_academic_transition:
                sentence_str = self.add_academic_transitions(sentence_str)
            
            # 4. Add sentence variation (occasionally reorder short sentences)
            if random.random() < 0.15 and ',' in sentence_str:
                sentence_str = self.add_sentence_variation(sentence_str)

            # Passive voice disabled for now due to grammar issues
            # if use_passive and random.random() < self.p_passive:
            #     sentence_str = self.convert_to_passive(sentence_str)

            transformed_sentences.append(sentence_str)

        # Join sentences with proper spacing
        result = ' '.join(transformed_sentences)
        
        # Clean up any double spaces
        result = re.sub(r'\s+', ' ', result).strip()
        
        # Fix spacing around punctuation (but not inside quotes)
        result = re.sub(r'\s+([.,!?;:])', r'\1', result)  # Remove space before punctuation
        result = re.sub(r'([.,!?;:])(?=[A-Za-z])', r'\1 ', result)  # Add space after punctuation if missing
        
        return result

    def expand_contractions(self, sentence):
        import re
        # DON'T touch possessives! Only expand actual contractions
        # Order matters: do specific patterns first, then general patterns
        contractions = [
            # Negatives
            (r"\bwon'?t\b", "will not"),
            (r"\bcan'?t\b", "cannot"),
            (r"\bshan'?t\b", "shall not"),
            (r"\bain'?t\b", "is not"),
            (r"\b(\w+)n'?t\b", r"\1 not"),  # Generic n't pattern
            
            # Pronouns + 'm
            (r"\bI'?m\b", "I am"),
            
            # Pronouns + 're  
            (r"\b(you|we|they)'?re\b", r"\1 are"),
            
            # Pronouns + 'll
            (r"\b(I|you|he|she|it|we|they)'?ll\b", r"\1 will"),
            
            # Pronouns + 've
            (r"\b(I|you|we|they)'?ve\b", r"\1 have"),
            
            # Pronouns + 'd
            (r"\b(I|you|he|she|it|we|they)'?d\b", r"\1 would"),
        ]
        
        # Apply contractions with word boundaries (case insensitive)
        for pattern, replacement in contractions:
            sentence = re.sub(pattern, replacement, sentence, flags=re.IGNORECASE)
        
        return sentence

    def add_sentence_variation(self, sentence):
        """Occasionally restructure sentences for more natural flow"""
        import re
        # Simple variation: if sentence has introductory phrase, sometimes keep it
        # This is very conservative to avoid breaking grammar
        return sentence
    
    def add_academic_transitions(self, sentence):
        import re
        # Don't add transitions to sentences starting with pronouns, names, or common words
        skip_patterns = [r'^(She|He|It|They|I|You|We|Her|His|Their|The|A|An|This|That|These|Those)\b']
        
        # Check if sentence starts with any skip pattern
        should_skip = any(re.match(pattern, sentence, re.IGNORECASE) for pattern in skip_patterns)
        
        # Only add transition if appropriate and sentence doesn't start with common words
        if (sentence and sentence[0].isupper() and not sentence.startswith('"') 
            and not should_skip and len(sentence.split()) > 5):  # Only for longer sentences
            transition = random.choice(self.academic_transitions)
            # Lowercase the first letter of the sentence after transition
            return f"{transition} {sentence[0].lower()}{sentence[1:]}"
        return sentence

    def convert_to_passive(self, sentence):
        # Disabled: passive voice conversion was creating grammatical errors
        # TODO: Implement proper passive voice with verb conjugation
        return sentence

    def replace_with_synonyms(self, sentence):
        import re
        
        # Words that should NEVER be replaced (common, important words)
        blacklist = {'sound', 'sounds', 'right', 'left', 'time', 'place', 'thing', 'things', 
                     'way', 'eyes', 'eye', 'hand', 'hands', 'head', 'face', 'light', 'lights',
                     'door', 'room', 'night', 'day', 'moment', 'second', 'minute'}
        
        tokens = word_tokenize(sentence)
        pos_tags = nltk.pos_tag(tokens)

        new_tokens = []
        for (word, pos) in pos_tags:
            word_lower = word.lower()
            
            # Skip blacklisted words
            if word_lower in blacklist:
                new_tokens.append(word)
                continue
            
            # Only replace adjectives (J), singular nouns (NN), and adverbs (RB)
            # SKIP PLURAL NOUNS (NNS) to preserve plurals!
            # Also skip proper nouns (NNP, NNPS) and possessives
            if pos in ('JJ', 'JJR', 'JJS', 'NN', 'RB', 'RBR', 'RBS') and wordnet.synsets(word) and len(word) > 4:
                if random.random() < 0.45:  # 45% chance for synonym replacement
                    synonyms = self._get_synonyms(word, pos)
                    if synonyms:
                        best_synonym = self._select_closest_synonym(word, synonyms)
                        if best_synonym and best_synonym.lower() != word_lower:
                            # Preserve capitalization
                            if word[0].isupper():
                                best_synonym = best_synonym.capitalize()
                            new_tokens.append(best_synonym)
                        else:
                            new_tokens.append(word)
                    else:
                        new_tokens.append(word)
                else:
                    new_tokens.append(word)
            else:
                new_tokens.append(word)

        # Simple join with intelligent spacing
        result = ""
        for i, token in enumerate(new_tokens):
            if i == 0:
                result += token
            elif token in '.,!?;:\'")':
                result += token
            elif new_tokens[i-1] in '(\'"':
                result += token
            else:
                result += ' ' + token
        
        return result

    def _get_synonyms(self, word, pos):
        wn_pos = None
        if pos.startswith('J'):
            wn_pos = wordnet.ADJ
        elif pos.startswith('N'):
            wn_pos = wordnet.NOUN
        elif pos.startswith('R'):
            wn_pos = wordnet.ADV
        elif pos.startswith('V'):
            wn_pos = wordnet.VERB

        synonyms = set()
        for syn in wordnet.synsets(word, pos=wn_pos):
            for lemma in syn.lemmas():
                lemma_name = lemma.name().replace('_', ' ')
                if lemma_name.lower() != word.lower():
                    synonyms.add(lemma_name)
        return list(synonyms)

    def _select_closest_synonym(self, original_word, synonyms):
        if not synonyms:
            return None
        # Filter out synonyms that are too different in length or structure
        filtered_synonyms = [s for s in synonyms if len(s.split()) == 1 and abs(len(s) - len(original_word)) <= 3]
        if not filtered_synonyms:
            return None
            
        original_emb = self.model.encode(original_word, convert_to_tensor=True)
        synonym_embs = self.model.encode(filtered_synonyms, convert_to_tensor=True)
        cos_scores = util.cos_sim(original_emb, synonym_embs)[0]
        max_score_index = cos_scores.argmax().item()
        max_score = cos_scores[max_score_index].item()
        # Increased threshold from 0.5 to 0.7 for better quality
        if max_score >= 0.7:
            return filtered_synonyms[max_score_index]
        return None
