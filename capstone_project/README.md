# 📄 AI Resume Critic — Tech-Roast

LIVE DEMO : https://ai-multiverse-4kczxxqgsg9smq4bcj2db4.streamlit.app/

An AI-powered resume analysis tool that evaluates a candidate's resume against a target Job Description and provides **ruthless recruiter-style feedback**.

The app uses **Google Gemini AI** to identify skill gaps, missing keywords, weak resume bullets, red flags, strengths, and actionable improvements.

## 🚀 Features

- 📄 Upload resume as a PDF
- 📝 Paste resume text directly
- 💼 Paste a target Job Description
- 🤖 Gemini-powered resume analysis
- 🎯 Overall Resume Score
- 📊 ATS Compatibility Score
- 🧠 Skill Match analysis
- 🔎 Missing keyword detection
- 💀 Ruthless "Tech-Roast" of weak bullet points
- 🚨 Biggest resume red flags
- 💎 Strongest parts of the resume
- 🛠️ Top 5 improvements
- 🎯 Shortlist / Reject recommendation
- 💬 Recruiter-style analysis and suggestions
- 📈 Resume Performance Dashboard

## 🛠️ Tech Stack

- **Python**
- **Streamlit**
- **Google Gemini API**
- **Pandas**
- **PyPDF**
- **python-dotenv**

## 🧠 How It Works

```text
Resume PDF / Text
        ↓
Resume Text Extraction
        ↓
Target Job Description
        ↓
Google Gemini AI
        ↓
Resume vs JD Analysis
        ↓
┌─────────────────────────────┐
│ Overall Score               │
│ ATS Compatibility           │
│ Skill Match                 │
│ Missing Keywords            │
│ Weak Bullet Points          │
│ Red Flags                   │
│ Strengths                   │
│ Tech-Roast                   │
│ Top Improvements             │
│ Shortlist Verdict            │
└─────────────────────────────┘
        ↓
Interactive Streamlit Dashboard
