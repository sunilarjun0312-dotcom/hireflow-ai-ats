import os
import shutil
from fastapi import FastAPI, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .database import engine, Base, get_db
from . import models, schemas
from .resume_parser import extract_text_from_pdf, analyze_resume_with_ai

# Create database tables automatically on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="HireFlow AI - Recruitment System", version="1.0")

@app.get("/")
def read_root():
    return {"message": "Welcome to HireFlow AI Recruitment System API!"}

# 1. Post a New Job (Recruiter)
@app.post("/jobs/", response_model=schemas.JobResponse)
def create_job(job: schemas.JobCreate, db: Session = Depends(get_db)):
    db_job = models.Job(
        title=job.title,
        description=job.description,
        required_skills=job.required_skills
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

# 2. Get All Jobs (Candidate / Recruiter)
@app.get("/jobs/", response_model=List[schemas.JobResponse])
def get_jobs(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    jobs = db.query(models.Job).offset(skip).limit(limit).all()
    return jobs

# 3. Apply for a Job with Resume PDF & AI Scoring
@app.post("/apply/{job_id}", response_model=schemas.ApplicationResponse)
async def apply_to_job(
    job_id: int,
    candidate_email: str = Form(...),
    resume: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Check if job exists
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # Find or create candidate user
    user = db.query(models.User).filter(models.User.email == candidate_email).first()
    if not user:
        user = models.User(email=candidate_email, hashed_password="dummy_password", role="candidate")
        db.add(user)
        db.commit()
        db.refresh(user)

    # Save uploaded resume PDF locally
    os.makedirs("uploaded_resumes", exist_ok=True)
    file_path = os.path.join("uploaded_resumes", resume.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(resume.file, buffer)

    # Extract text from PDF & run AI Analysis
    resume_text = extract_text_from_pdf(file_path)
    ai_result = analyze_resume_with_ai(resume_text, job.description)

    # Save Application to Database with ATS Score
    db_application = models.Application(
        job_id=job.id,
        candidate_id=user.id,
        resume_path=file_path,
        match_score=ai_result.get("match_score", 0.0),
        matched_skills=ai_result.get("matched_skills", ""),
        missing_skills=ai_result.get("missing_skills", ""),
        status="Applied"
    )
    db.add(db_application)
    db.commit()
    db.refresh(db_application)

    return db_application