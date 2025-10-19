from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import sys
import os

# Add the transformer directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from transformer.app import AcademicTextHumanizer, download_nltk_resources
from nltk.tokenize import word_tokenize

# Download NLTK resources on startup
download_nltk_resources()

app = FastAPI(title="AI Text Humanizer API (Full Version)", version="1.0.0")

# Enable CORS for WordPress integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your WordPress domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the humanizer with ML models (balanced quality + effectiveness)
humanizer = AcademicTextHumanizer(
    p_passive=0.0,  # Disabled due to grammar issues
    p_synonym_replacement=0.5,  # Balanced for quality
    p_academic_transition=0.1  # Very minimal transitions
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

@app.get("/")
async def root():
    return {
        "message": "AI Text Humanizer API (Full Version with ML Models)",
        "version": "1.0.0",
        "note": "Advanced humanization with spaCy, NLTK, and sentence transformers",
        "endpoints": {
            "/humanize": "POST - Humanize text",
            "/health": "GET - Health check"
        }
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "version": "full"}

@app.post("/humanize", response_model=TextResponse)
async def humanize_text_endpoint(request: TextRequest):
    try:
        if not request.text.strip():
            raise HTTPException(status_code=400, detail="Text cannot be empty")
        
        # Input statistics
        input_word_count = len(word_tokenize(request.text, language='english', preserve_line=True))
        input_sentence_count = len(list(humanizer.nlp(request.text).sents))
        
        # Transform the text with ML models
        humanized = humanizer.humanize_text(
            request.text,
            use_passive=request.use_passive,
            use_synonyms=request.use_synonyms
        )
        
        # Output statistics
        output_word_count = len(word_tokenize(humanized, language='english', preserve_line=True))
        output_sentence_count = len(list(humanizer.nlp(humanized).sents))
        
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
