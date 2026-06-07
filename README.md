# RecruitAI — Smart Resume Screening

> AI-powered candidate screening that ranks resumes against a job description in seconds — built with Streamlit and powered by Groq · Llama 3.3.

---

## Screenshots

### Landing Page
![RecruitAI Landing Page](assets/screenshot_hero.png)

### Upload Interface
![Upload Job Description and Resumes](assets/screenshot_upload.png)

### Screening Results
![AI-Ranked Candidate Results](assets/screenshot_results.png)

---

## What It Does

Paste a job description, upload any number of candidate PDFs, and RecruitAI returns a ranked shortlist — instantly. Each candidate gets:

- **Match score** (0–100) with a colour-coded progress bar
- **Top strengths** — specific skills that align with the role
- **Skill gaps** — what the candidate is missing
- **Summary** — a concise 2–3 sentence honest assessment

No manual screening. No spreadsheets. Just results.

---

## Features

- 📋 Paste any job description — the more detail, the better the analysis
- 📁 Upload multiple PDF resumes at once
- 🏆 Candidates ranked #1, #2, #3... by match score
- 🟢 Green / 🟡 Amber / 🔴 Red score colouring for instant visual triage
- 🏷️ Skill tags displayed as clean pills (not bullet points)
- ⚡ Powered by Groq's ultra-fast Llama 3.3-70b inference
- 🎨 Polished dark UI matching a production-grade design

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend / UI | Streamlit |
| AI Model | Llama 3.3-70b-versatile via Groq API |
| PDF Parsing | pdfplumber |
| Environment | python-dotenv |
| Language | Python 3.10+ |

---

## Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/AryanLovesCoding/RecruitAI.git
cd RecruitAI
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Get a free Groq API key

Go to [console.groq.com](https://console.groq.com) → Sign up → Create API Key. It's free with generous limits (~1,000 requests/day on the free tier).

### 4. Add your API key

```bash
cp .env.example .env
```

Open `.env` and replace the placeholder:

```
GROQ_API_KEY=your_actual_groq_api_key_here
```

### 5. Run the app

```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## Project Structure

```
RecruitAI/
├── app.py               # Main Streamlit application
├── requirements.txt     # Python dependencies
├── .env                 # Your API key (never committed)
├── .env.example         # Safe template for others to copy
├── .gitignore           # Keeps .env out of GitHub
├── assets/
│   ├── screenshot_hero.png
│   ├── screenshot_upload.png
│   └── screenshot_results.png
└── README.md            # This file
```

---

## How It Works

1. **PDF extraction** — `pdfplumber` pulls raw text from each uploaded resume
2. **Prompt construction** — job description + all resume texts are bundled into a structured prompt
3. **AI analysis** — Groq's Llama 3.3-70b model analyses every resume against the JD simultaneously and returns a ranked JSON array
4. **Rendering** — Streamlit renders each candidate as a card with score, bar, strengths, gaps, and summary

---

## Requirements

```
streamlit>=1.35.0
groq>=0.9.0
pdfplumber>=0.11.0
python-dotenv>=1.0.0
```

---

## Security

- Your `GROQ_API_KEY` lives only in `.env` which is listed in `.gitignore` and **never pushed to GitHub**
- `.env.example` is the safe placeholder file that gets committed instead
- No data is stored — everything is processed in memory and discarded after each session

---

## Developed By

**Aryan Ajmera**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/aryan-ajmera7)
[![Portfolio](https://img.shields.io/badge/Portfolio-7c3aed?style=for-the-badge&logo=google-chrome&logoColor=white)](https://aryanlovescoding.github.io/AryanWebsite/)

---

*Built with Streamlit · Groq · Llama 3.3*
