# Invoice Processor (simple)

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![AWS Textract](https://img.shields.io/badge/AWS_Textract-FF9900?logo=amazon-aws&logoColor=white)
![SpaCy](https://img.shields.io/badge/SpaCy-NLP-09A3D5?logo=spacy&logoColor=white)

## Description
This folder contains my contribution to a team project that extracts structured data from invoices using **AWS Textract** for OCR and **NLP (SpaCy + regex)** for field refinement.  
Later, **Gemini AI** was tested and used as a more reliable alternative for generating clean structured output.

## Files
- `textract_processor.py` — Textract OCR pipeline  
- `nlp_processor.py` — SpaCy + regex refinements  
- `nlp_utils.py` — helper utilities for NLP  
- `gemini_invoice.py` — improved version using Gemini AI

## Note
- This folder contains **only my part** of the team project.  
- The final `gemini_invoice.py` was **used together with another Textract module** in the team version.  
- Not a full application.

## Requirements
- Python 3.10+  
- boto3  
- spacy  
- google.generativeai

## Env / Requirements (minimal)
- `GEMINI_API_KEY` (if using `gemini_invoice.py`)  
- Python 3.10+, boto3, spacy, google.generativeai

