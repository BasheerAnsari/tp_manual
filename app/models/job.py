# models/job.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func,Enum,Date
from sqlalchemy.orm import relationship
from core_services.app.core.database import Base  # shared Base
from core_services.app.models.recruiter_model import Recruiter
from core_services.app.enums.job_status import JobStatus
from core_services.app.enums.job_type import JobType
from core_services.app.enums.industry import Industry

from sqlalchemy.dialects.postgresql import ARRAY as PG_ARRAY

class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, index=True) 
    # job_title = Column(String)
    # department = Column(String)                                                 # change to the FK , department id or department name 
    # job_description = Column(String)
    # required_skills = Column(String)                                            # store as CSV string for now , later JSON 
    # experience_level = Column(String)
    # location = Column(String)
    # employment_type = Column(String)
    posting_title = Column(String, nullable=False)
    department = Column(String, nullable=False)                            #FK departments
    title = Column(String, nullable=True)
    hiring_manager = Column(String, nullable=True)
    assigned_recuiter = Column(String, nullable=True)
    number_of_position = Column(String, nullable=True)
    target_date = Column(Date, nullable=False)
    date_opened = Column(Date, nullable=False)


    job_status = Column(Enum(JobStatus, name="job_status_enum"), nullable=False, default=JobStatus.DRAFT)
    job_type = Column(Enum(JobType, name="job_type_enum"), nullable=False)
    industry = Column(Enum(Industry, name="industry_enum"), nullable=False)
    
    work_experience = Column(String, nullable=False)
    required_skills = Column(PG_ARRAY(String), nullable=False)  # PostgreSQL ARRAY
    job_description = Column(String, nullable=False)
    requirements = Column(String, nullable=True)
    benefits = Column(String, nullable=True)
    
    city = Column(String, nullable=True)
    country = Column(String, nullable=True)
    state = Column(String, nullable=True)
    postal_code = Column(Integer, nullable=True)


    user_id = Column(Integer, ForeignKey("recruiters.id", ondelete= "CASCADE"), nullable=False)  # forignkey refereing the recruter table 

    user= relationship("Recruiter",backref="jobs")                               # relationship section

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )