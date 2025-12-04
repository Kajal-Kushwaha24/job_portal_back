from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db
from models.application import Application
from models.job import Job
from models.user import User

router = APIRouter(prefix="/apply", tags=["applications"])


class ApplyRequest(BaseModel):
    user_email: str
    job_id: int


class ApplyResponse(BaseModel):
    message: str
    application_id: int


@router.post("", response_model=ApplyResponse)
def apply_for_job(apply_data: ApplyRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == apply_data.user_email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    job = db.query(Job).filter(Job.id == apply_data.job_id).first()
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )

    existing_application = db.query(Application).filter(
        Application.user_email == apply_data.user_email,
        Application.job_id == apply_data.job_id
    ).first()

    if existing_application:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already applied for this job"
        )

    new_application = Application(
        user_email=apply_data.user_email,
        job_id=apply_data.job_id
    )

    db.add(new_application)
    db.commit()
    db.refresh(new_application)

    return ApplyResponse(
        message="Application submitted successfully",
        application_id=new_application.id
    )
