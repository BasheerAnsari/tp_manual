from fastapi import APIRouter, Depends, HTTPException,Query
from sqlalchemy.orm import Session
from core_services.app.schemas.job import JOB
from core_services.app.models.job import Job                                # SQLAlchemy model
from core_services.app.core.database import get_db  
from core_services.app.services.job_service import JobService
from core_services.app.shared.helper.api_response import api_response


job_router = APIRouter(prefix="/api/job", tags=["jobs"])


# Create Job
@job_router.post("/")
async def create_job(job: JOB, db: Session = Depends(get_db)):
    created_job = JobService.create_job(job, db)
    #return {"message": "Job created successfully", "job_id": created_job.id}
    return api_response(
        status_code=201,
        successful=True,
        message="Job created successfully",
        data={
            "job_id": created_job.id
        }
    )


# Get Job List
@job_router.get("/")
async def get_jobs(
    job_title: str | None = Query(default=None, description="Filter by job title"),
    location: str | None = Query(default=None, description="Filter by job location"),
    user_id: int | None = Query(...,description= "user_id is required"),               # user_id: int = Query(..., description="Recruiter user ID"),
    page: int = Query(default=1, ge=1, description="Page number"),
    per_page: int = Query(default=10, ge=1, le=100, description="Number of records per page"),
    db: Session = Depends(get_db)
):
    data = JobService.get_jobs(
        user_id=user_id,
        job_title=job_title,
        location=location,
        page=page,
        per_page=per_page,
        db=db
    )
    
    #return JobService.get_jobs(user_id,job_title, location, page, per_page, db)

    return api_response(
        status_code=200,
        successful=True,
        message="Jobs fetched successfully",
        data=data
    )