from fastapi import APIRouter, Depends, HTTPException,Query
from sqlalchemy.orm import Session
from core_services.app.schemas.job import JOB
from core_services.app.models.job import Job                                # SQLAlchemy model
from core_services.app.core.database import get_db  
from core_services.app.services.job_service import JobService
from core_services.app.shared.helper.api_response import api_response

from fastapi import UploadFile, File
import shutil, uuid, os
from core_services.app.services.job_service import JobService
from core_services.app.shared.helper.api_response import api_response
from langchain_community.document_loaders import PyPDFLoader, TextLoader
import docx2txt


job_router = APIRouter(prefix="/api/job", tags=["jobs"])


def load_jd_text(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        docs = PyPDFLoader(file_path).load()
        return "\n".join(d.page_content for d in docs)

    if ext == ".docx":
        return docx2txt.process(file_path)

    return TextLoader(file_path, encoding="utf-8").load()[0].page_content

@job_router.post("/extract-jd")
async def extract_job_from_jd(file: UploadFile = File(...)):
    file_path = f"uploads/{uuid.uuid4()}_{file.filename}"

    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    jd_text = load_jd_text(file_path)
    extracted_job = JobService.extract_job_from_jd(jd_text)

    return api_response(
        status_code=200,
        successful=True,
        message="Job details extracted from JD",
        data=extracted_job
    )



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