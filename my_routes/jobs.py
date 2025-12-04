from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db
from models.job import Job
from models.user import User

router = APIRouter(prefix="/jobs", tags=["jobs"])


class JobCreate(BaseModel):
    title: str
    description: str
    location: str


class JobResponse(BaseModel):
    id: int
    title: str
    description: str
    location: str
    created_by: int
    created_at: datetime

    class Config:
        from_attributes = True


class JobCreateRequest(BaseModel):
    title: str
    description: str
    location: str
    recruiter_email: str


@router.post("", response_model=dict)
def create_job(job_data: JobCreateRequest, db: Session = Depends(get_db)):
    recruiter = db.query(User).filter(
        User.email == job_data.recruiter_email,
        User.role == "recruiter"
    ).first()

    if not recruiter:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only recruiters can create jobs"
        )

    new_job = Job(
        title=job_data.title,
        description=job_data.description,
        location=job_data.location,
        created_by=recruiter.id
    )

    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    return {
        "message": "Job created successfully",
        "job_id": new_job.id
    }


@router.get("", response_model=List[JobResponse])
def get_jobs(db: Session = Depends(get_db)):
    jobs = db.query(Job).all()
    return jobs
