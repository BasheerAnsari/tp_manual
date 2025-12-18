# models/job.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from core_services.app.core.database import Base  # shared Base
from core_services.app.models.recruiter_model import Recruiter

class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, index=True) 
    job_title = Column(String)
    department = Column(String)                                                 # change to the FK , department id or department name 
    job_description = Column(String)
    required_skills = Column(String)                                            # store as CSV string for now , later JSON 
    experience_level = Column(String)
    location = Column(String)
    employment_type = Column(String)
    user_id = Column(Integer, ForeignKey("recruiters.id", ondelete= "CASCADE"), nullable=False)  # forignkey refereing the recruter table 

    user= relationship("Recruiter",backref="jobs")                               # relationship section