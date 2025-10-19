from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import re

app = FastAPI(title="AI Text Humanizer API (Lite)", version="1.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextRequest(BaseModel):
    text: str
    use_passive: bool = False
    use_synonyms: bool = False

class TextResponse(BaseModel):
    original_text: str
    humanized_text: str
    input_word_count: int
    input_sentence_count: int
    output_word_count: int
    output_sentence_count: int

# Simple contraction map
CONTRACTIONS = {
    "n't": " not",
    "'re": " are",
    "'s": " is",
    "'ll": " will",
    "'ve": " have",
    "'d": " would",
    "'m": " am",
    "won't": "will not",
    "can't": "cannot",
    "don't": "do not",
    "doesn't": "does not",
    "didn't": "did not",
    "shouldn't": "should not",
    "wouldn't": "would not",
    "couldn't": "could not",
    "isn't": "is not",
    "aren't": "are not",
    "wasn't": "was not",
    "weren't": "were not",
    "haven't": "have not",
    "hasn't": "has not",
    "hadn't": "had not",
}

# Academic transitions
TRANSITIONS = [
    "Moreover,", "Additionally,", "Furthermore,", "Hence,",
    "Therefore,", "Consequently,", "Nonetheless,", "Nevertheless,",
]

def count_words(text):
    """Count words in text"""
    return len(text.split())

def count_sentences(text):
    """Count sentences in text"""
    return len(re.split(r'[.!?]+', text.strip()))

def expand_contractions(text):
    """Expand contractions in text"""
    expanded = text
    for contraction, expansion in CONTRACTIONS.items():
        # Case insensitive replacement
        pattern = re.compile(re.escape(contraction), re.IGNORECASE)
        expanded = pattern.sub(expansion, expanded)
    return expanded

def add_transitions(text):
    """Add academic transitions to some sentences"""
    sentences = re.split(r'([.!?]+)', text)
    result = []
    
    import random
    for i, sentence in enumerate(sentences):
        if sentence.strip() and not re.match(r'^[.!?]+$', sentence):
            # 30% chance to add transition
            if random.random() < 0.3 and i > 0:
                transition = random.choice(TRANSITIONS)
                result.append(f" {transition} {sentence.strip()}")
            else:
                result.append(sentence)
        else:
            result.append(sentence)
    
    return ''.join(result)

def humanize_text(text, use_passive=False, use_synonyms=False):
    """Humanize the text with basic transformations"""
    # Expand contractions
    humanized = expand_contractions(text)
    
    # Add academic transitions
    humanized = add_transitions(humanized)
    
    # Clean up extra spaces
    humanized = re.sub(r'\s+', ' ', humanized).strip()
    
    return humanized

@app.get("/")
async def root():
    return {
        "message": "AI Text Humanizer API (Lite Version)",
        "version": "1.0.0",
        "note": "Lightweight version without ML models",
        "endpoints": {
            "/humanize": "POST - Humanize text",
            "/health": "GET - Health check"
        }
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "version": "lite"}

@app.post("/humanize", response_model=TextResponse)
async def humanize_endpoint(request: TextRequest):
    try:
        if not request.text.strip():
            raise HTTPException(status_code=400, detail="Text cannot be empty")
        
        # Input statistics
        input_word_count = count_words(request.text)
        input_sentence_count = count_sentences(request.text)
        
        # Transform the text
        humanized = humanize_text(
            request.text,
            use_passive=request.use_passive,
            use_synonyms=request.use_synonyms
        )
        
        # Output statistics
        output_word_count = count_words(humanized)
        output_sentence_count = count_sentences(humanized)
        
        return TextResponse(
            original_text=request.text,
            humanized_text=humanized,
            input_word_count=input_word_count,
            input_sentence_count=input_sentence_count,
            output_word_count=output_word_count,
            output_sentence_count=output_sentence_count
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing text: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
