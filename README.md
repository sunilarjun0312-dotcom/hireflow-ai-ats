# 🚀 HireFlow AI — Intelligent Applicant Tracking System (ATS)

An AI-powered full-stack Applicant Tracking System built with **FastAPI** and **React.js**. HireFlow AI automates resume screening by parsing PDF resumes, extracting candidate skills, and calculating an ATS match score against job descriptions.

---

## ✨ Key Features

* **Automated PDF Resume Parsing:** Extracts text and key technical skills directly from uploaded PDF resumes.
* **AI Skill Matching & Scoring:** Compares candidate resumes against job requirements to generate an instant percentage match score.
* **Skill Gap Analysis:** Clearly highlights **Matched Skills** and **Missing Skills** for quick recruiter decision-making.
* **Interactive Recruiter Dashboard:** Clean React frontend to select open roles, upload resumes, and view real-time evaluation results.
* **RESTful API Architecture:** High-performance FastAPI backend with interactive Swagger documentation (`/docs`).

---

## 🛠️ Tech Stack

* **Frontend:** React.js, Axios, CSS3
* **Backend:** Python 3.11, FastAPI, Uvicorn, SQLAlchemy
* **Database:** SQLite
* **Resume Processing:** PDF text extraction & NLP keyword matching

---

## 📂 Project Structure

```text
HireFlowProject/
├── backend/
│   ├── app/
│   │   ├── main.py            # FastAPI routes & CORS configuration
│   │   ├── database.py        # SQLite database connection
│   │   ├── models.py          # SQLAlchemy ORM models
│   │   ├── schemas.py         # Pydantic data validation schemas
│   │   └── resume_parser.py   # PDF text extraction & ATS scoring logic
│   └── requirements.txt       # Python dependencies
├── frontend/
│   ├── public/
│   └── src/
│       ├── App.js             # Main ATS dashboard & API integration
│       └── App.css            # Styling
└── .gitignore
