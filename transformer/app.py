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

            # 2. Add academic transitions (only to some sentences, not the first)
            if i > 0 and random.random() < self.p_academic_transition:
                sentence_str = self.add_academic_transitions(sentence_str)

            # 3. Optionally replace words with synonyms (excluding verbs to preserve grammar)
            if use_synonyms and random.random() < self.p_synonym_replacement:
                sentence_str = self.replace_with_synonyms(sentence_str)

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
        # Comprehensive contraction map (handles both with and without apostrophes)
        contractions = [
            (r"\bwon'?t\b", "will not"),
            (r"\bcan'?t\b", "cannot"),
            (r"\bdon'?t\b", "do not"),
            (r"\bdoesn'?t\b", "does not"),
            (r"\bdidn'?t\b", "did not"),
            (r"\bshouldn'?t\b", "should not"),
            (r"\bwouldn'?t\b", "would not"),
            (r"\bcouldn'?t\b", "could not"),
            (r"\bisn'?t\b", "is not"),
            (r"\baren'?t\b", "are not"),
            (r"\bwasn'?t\b", "was not"),
            (r"\bweren'?t\b", "were not"),
            (r"\bhaven'?t\b", "have not"),
            (r"\bhasn'?t\b", "has not"),
            (r"\bhadn'?t\b", "had not"),
            (r"\bI'?m\b", "I am"),
            (r"\byou'?re\b", "you are"),
            (r"\bhe'?s\b", "he is"),
            (r"\bshe'?s\b", "she is"),
            (r"\bit'?s\b", "it is"),
            (r"\bwe'?re\b", "we are"),
            (r"\bthey'?re\b", "they are"),
            (r"\bI'?ll\b", "I will"),
            (r"\byou'?ll\b", "you will"),
            (r"\bhe'?ll\b", "he will"),
            (r"\bshe'?ll\b", "she will"),
            (r"\bit'?ll\b", "it will"),
            (r"\bwe'?ll\b", "we will"),
            (r"\bthey'?ll\b", "they will"),
            (r"\bI'?ve\b", "I have"),
            (r"\byou'?ve\b", "you have"),
            (r"\bwe'?ve\b", "we have"),
            (r"\bthey'?ve\b", "they have"),
            (r"\bI'?d\b", "I would"),
            (r"\byou'?d\b", "you would"),
            (r"\bhe'?d\b", "he would"),
            (r"\bshe'?d\b", "she would"),
            (r"\bwe'?d\b", "we would"),
            (r"\bthey'?d\b", "they would"),
        ]
        
        # Apply contractions with word boundaries
        for pattern, replacement in contractions:
            sentence = re.sub(pattern, replacement, sentence, flags=re.IGNORECASE)
        
        return sentence

    def add_academic_transitions(self, sentence):
        import re
        transition = random.choice(self.academic_transitions)
        # Only add transition if sentence starts with a capital letter and isn't a quote
        if sentence and sentence[0].isupper() and not sentence.startswith('"'):
            # Lowercase the first letter of the sentence after transition
            return f"{transition} {sentence[0].lower()}{sentence[1:]}"
        return sentence

    def convert_to_passive(self, sentence):
        # Disabled: passive voice conversion was creating grammatical errors
        # TODO: Implement proper passive voice with verb conjugation
        return sentence

    def replace_with_synonyms(self, sentence):
        import re
        
        tokens = word_tokenize(sentence)
        pos_tags = nltk.pos_tag(tokens)

        new_tokens = []
        for (word, pos) in pos_tags:
            # Only replace adjectives (J), nouns (N), and adverbs (R) - SKIP VERBS to preserve grammar
            # Also skip proper nouns (NNP, NNPS) and possessives
            if pos.startswith(('J', 'N', 'RB')) and not pos.startswith(('NNP', 'NNPS')) and wordnet.synsets(word) and len(word) > 3:
                if random.random() < 0.35:  # 35% chance for synonym replacement (quality over quantity)
                    synonyms = self._get_synonyms(word, pos)
                    if synonyms:
                        best_synonym = self._select_closest_synonym(word, synonyms)
                        if best_synonym:
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
