#!/bin/bash
set -e

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Downloading spaCy language model..."
python -m spacy download en_core_web_sm

echo "Build complete! Full version with ML models ready."
