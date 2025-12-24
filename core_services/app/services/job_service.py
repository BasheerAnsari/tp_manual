import os
from sqlalchemy.orm import Session
from sqlalchemy import and_
#from fastapi import HTTPException

from core_services.app.models.job import Job
from core_services.app.schemas.job import JOB
from core_services.app.shared.helper.pagination import Paginator

from langchain_openai import AzureChatOpenAI
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
import json
import re


class JobService:

    @staticmethod
    def extract_job_from_jd(jd_text: str) -> dict:
        llm = AzureChatOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
            api_version="2024-12-01-preview"
        )
        # llm = ChatOllama(
        #     model="llama3.2:1b",
        #     base_url="http://localhost:11434"
        # )

        prompt = ChatPromptTemplate.from_template("""
You are an HR system.

Extract job details from the Job Description below.

Return STRICT JSON with these fields:
- job_title
- department
- job_description
- required_skills
- experience_level
- location
- employment_type

JD:
{jd_text}
""")

        response = llm.invoke(prompt.format(jd_text=jd_text))

        match = re.search(r"\{.*\}", response.content, re.DOTALL)
        if not match:
            raise ValueError("Invalid JSON returned by Ollama")

        return json.loads(response.content)

    @staticmethod
    def create_job(job: JOB, db: Session):
        try:
            db_job = Job(
                job_title=job.job_title,
                department=job.department,
                job_description=job.job_description,
                required_skills=job.required_skills,
                experience_level=job.experience_level,
                location=job.location,
                employment_type=job.employment_type,
                user_id=job.user_id
            )

            db.add(db_job)
            db.commit()
            db.refresh(db_job)

            return db_job

        except Exception as e:
            db.rollback()
            #raise HTTPException(status_code=500, detail=f"Error creating job: {str(e)}")
            raise ValueError("Failed to create job")


    @staticmethod
    def get_jobs(user_id: int, job_title: str, location: str, page: int, per_page: int, db: Session):
        try:
            query = db.query(Job)

            filters = [Job.user_id == user_id]  

            if job_title:   
                filters.append(Job.job_title.ilike(f"%{job_title}%"))

            if location:    
                filters.append(Job.location.ilike(f"%{location}%"))
             
            query = query.filter(and_(*filters))

            return Paginator.pagination(query,page,per_page)


        except Exception as e:
            #raise HTTPException(status_code=500, detail=f"Error fetching jobs: {str(e)}")
            raise ValueError("Failed to fetch jobs")