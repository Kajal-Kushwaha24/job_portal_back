from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String(255), nullable=False, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)

    job = relationship("Job", back_populates="applications")

