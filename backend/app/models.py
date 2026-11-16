from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="candidate")  # "recruiter" or "candidate"
    created_at = Column(DateTime, default=datetime.utcnow)

    applications = relationship("Application", back_populates="candidate")

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    required_skills = Column(String, nullable=False)  # comma separated skills
    created_at = Column(DateTime, default=datetime.utcnow)

    applications = relationship("Application", back_populates="job")

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    candidate_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    resume_path = Column(String, nullable=False)
    match_score = Column(Float, default=0.0)
    matched_skills = Column(Text, nullable=True)
    missing_skills = Column(Text, nullable=True)
    status = Column(String, default="Applied")  # Applied, Shortlisted, Rejected
    created_at = Column(DateTime, default=datetime.utcnow)

    job = relationship("Job", back_populates="applications")
    candidate = relationship("User", back_populates="applications")