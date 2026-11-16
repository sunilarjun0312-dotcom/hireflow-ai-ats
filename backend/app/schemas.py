from pydantic import BaseModel
from typing import Optional

class JobCreate(BaseModel):
    title: str
    description: str
    required_skills: str

class JobResponse(JobCreate):
    id: int

    class Config:
        from_attributes = True

class ApplicationResponse(BaseModel):
    id: int
    job_id: int
    candidate_id: int
    match_score: float
    matched_skills: Optional[str] = None
    missing_skills: Optional[str] = None
    status: str

    class Config:
        from_attributes = True