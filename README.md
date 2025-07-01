
# AIResumeChecker — AI-Powered Resume Analyzer

**AIResumeChecker** is an intelligent web application that allows users to upload resumes and job descriptions, analyzes both using NLP, and provides keyword insights, skill match percentage, and improvement suggestions.

Built with **Python**, **Flask**, **spaCy/BERT**, and **MongoDB/PostgreSQL**.

---

##  Features

- Upload resume in **PDF/DOCX** format  
- Paste or upload **job description**  
- Extract **skills**, **keywords**, and **entities** using **spaCy or BERT**  
- Compare and calculate **resume-job match score**  
-  Visual feedback on **missing skills** and improvements  
-  Downloadable **PDF report**  
-  (Optional) GPT-based suggestions for better resume alignment

---

##  Tech Stack

| Layer          | Technologies                                |
|----------------|---------------------------------------------|
| Backend        | Python, Flask                               |
| NLP Engine     | spaCy, NLTK, Hugging Face Transformers (BERT) |
| File Parsing   | pdfminer.six, python-docx                   |
| Database       | MongoDB / PostgreSQL                        |
| Frontend       | HTML, CSS, Bootstrap                        |
| Visualization  | Chart.js / Matplotlib (optional)            |

---

## Folder Structure
resume-analyzer/
├── app/
│ ├── static/
│ ├── templates/
│ ├── routes.py
│ ├── utils.py # NLP & comparison logic
│ ├── models.py # Database models
│ └── init.py
├── uploads/ # Uploaded resumes
├── resume_parser.py # Resume file handler
├── requirements.txt
├── config.py
└── run.py

---

## Getting Started

###  Installation

1. **Clone the Repository**

```bash
git clone https://github.com/yourusername/resume-analyzer.git
cd resume-analyzer
python -m venv venv
source venv/bin/activate   # on Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py
Requirements
Python 3.8+

Flask

spaCy (en_core_web_sm)

pdfminer.six

python-docx

MongoDB or PostgreSQL

Optional: Transformers, OpenAI API

To-Do
 Add JWT-based user login

 Resume formatting checker

 GPT-based suggestions for resume rewrite

 Email resume rating reports
