# Resume Analyzer — AI-Based ATS Simulation System

An AI-powered web application that simulates an Applicant Tracking 
System (ATS). Upload your resume and a job description to get your 
ATS match score, keyword analysis and improvement suggestions.

## Live Demo
Run locally at http://127.0.0.1:5000

## Tech Stack
- Python + Flask
- spaCy (NLP)
- scikit-learn (TF-IDF + Cosine Similarity)
- PyPDF2 (PDF Extraction)
- SQLite (Database)
- HTML + CSS + JavaScript

## How To Run

### 1. Clone the repository
git clone https://github.com/aasi7376/resume-analyzer.git
cd resume-analyzer

### 2. Install dependencies
pip install flask PyPDF2 spacy scikit-learn werkzeug
python -m spacy download en_core_web_sm

### 3. Run the app
python app.py

### 4. Open in browser
http://127.0.0.1:5000

## Modules
| Module | File | Description |
|--------|------|-------------|
| 1 | analyzer | Upload resume and get ATS score |
| 2 | extractor.py | PDF text extraction using PyPDF2 |
| 3 | preprocessor.py | NLP text cleaning using spaCy |
| 4 | matcher.py | Keyword matching between resume and JD |
| 5 | scorer.py | TF-IDF and cosine similarity scoring |
| 6 | result | Full result visualization |
| 7 | dashboard | Analysis history stored in SQLite |

## Project Structure
resume_analyzer/
├── app.py
├── extractor.py
├── preprocessor.py
├── matcher.py
├── scorer.py
├── suggestions.py
├── database.py
├── requirements.txt
├── templates/
│   ├── base.html
│   ├── landing.html
│   ├── analyzer.html
│   ├── extractor.html
│   ├── preprocessor.html
│   ├── matcher.html
│   ├── scorer.html
│   ├── result.html
│   └── dashboard.html
└── static/
    ├── css/style.css
    └── js/main.js
