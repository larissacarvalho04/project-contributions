# Invoice Processor (simple)

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white) ![AWS Textract](https://img.shields.io/badge/AWS_Textract-FF9900?logo=amazon-aws&logoColor=white) ![SpaCy](https://img.shields.io/badge/SpaCy-NLP-09A3D5?logo=spacy&logoColor=white) ![Gemini AI](https://img.shields.io/badge/Gemini_AI-FF6F61?logo=google&logoColor=white)

## Description
Simple module that extracts structured data from invoices using AWS Textract, SpaCy-based NLP and (optionally) Gemini AI.  
The first three files are **prototypes**. The fourth (`gemini_invoice.py`) was **adapted for team use**.

## Files
- `textract_processor.py` — Textract pipeline (OCR + expense fields)  
- `nlp_processor.py` — SpaCy + regex to extract/complete fields  
- `nlp_utils.py` — small helpers for the NLP matcher and extraction  
- `gemini_invoice.py` — uses Gemini to produce a final JSON (team-adapted)

## Note
This folder contains only my part of the work. Not a full application.

## Env / Requirements (minimal)
- `GEMINI_API_KEY` (if using `gemini_invoice.py`)  
- Python 3.10+, boto3, spacy, google.generativeai

