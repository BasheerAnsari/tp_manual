from pydantic import BaseModel, Field, conint
from typing import List,Optional
from datetime import date
from core_services.app.enums.job_type import JobType
from core_services.app.enums.job_status import JobStatus
from core_services.app.enums.industry import Industry

# class JOB(BaseModel):
#     job_title: str = Field(..., min_length=1, description="Job title cannot be empty")
#     department: str = Field(..., min_length=1, description="Department cannot be empty")
#     job_description: str = Field(..., min_length=1, description="Job description cannot be empty")
#     required_skills: List[str] = Field(..., description="At least one skill is required")                     # add  Field(..., min_items=1)
#     experience_level: str = Field(..., min_length=1, description="Experience level cannot be empty")
#     location: str = Field(..., min_length=1, description="Location cannot be empty")
#     employment_type: str = Field(..., min_length=1, description="Employment type cannot be empty")
#     user_id: conint(gt=0) = Field(..., description="User ID must be greater than 0")



class JOB(BaseModel):
    posting_title: str = Field(..., min_length=3, description="Job title cannot be empty")
    department: str = Field(..., min_length=3, description="Department cannot be empty")
    title: Optional[str] = Field(
        default=None,
        min_length=1,
        description="Job title (optional)"
    )
    hiring_manager: Optional[str] = Field(
        default = None,
        min_length = 3,
        description = "hiring manager (optional)",
    )
    assigned_recuiter: Optional[str] = Field(
        default = None,
        min_length = 3,
        description = "assigned recuiter (optional)",
    )
    number_of_position : Optional[str] = Field(
        default = None,
        min_length = 1,
        description = "number_of_position (optional)",
    )
    target_date: date = Field(
        ...,
        description="Target completion date (mandatory)"
    )
    date_opened: date = Field(
        ...,
        description="Date Opening date (mandatory)"
    )
    job_status: str = Field(
        description="Current status of the job opening"
    )
    job_type: str = Field(
        ...,
        description="Type of the job (Full-Time / Part-Time / Contract / Intern / Temporary)"
    )
    industry: str = Field(..., description="Industry of the job")
    work_experience : str = Field(...,min_length= 1, description="work_experience cannot be empty")
    required_skills: List[str] = Field(..., description="At least one skill is required")
    job_description: str = Field(..., min_length=1, description="Job description cannot be empty")
    requirements: Optional[str] = Field(default=None, description="Job requirements (optional)")
    benefits: Optional[str] = Field(default= None, description= "benefits offered")
    city: Optional[str] = Field(default= None, description= "city is optional")
    country: Optional[str] = Field(default= None, description= "Country is optional")
    state: Optional[str] = Field(default= None, description= "state is optional")
    postal_code: Optional[int] = Field(default=None, description="Postal code of the job location (optional)")    
    user_id: conint(gt=0) = Field(..., description="User ID must be greater than 0")

    class Config:
        use_enum_values = True

class JobExtractResponse(BaseModel):
    job_title: str
    department: str
    job_description: str
    required_skills: List[str]
    experience_level: str
    location: str
    employment_type: str