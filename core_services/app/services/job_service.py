import os
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
#from fastapi import HTTPException

from core_services.app.models.job import Job
from core_services.app.schemas.job import JOB
from core_services.app.shared.helper.pagination import Paginator

from langchain_openai import AzureChatOpenAI
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
        

        prompt = ChatPromptTemplate.from_template("""
You are an HR system.

Your task is to extract structured job information from the provided content.

STRICT RULES:
- Return ONLY valid JSON (no markdown, no explanations)
- Do NOT invent information that is not present
- Use professional HR language
- Keep values concise and clean

FIELD-SPECIFIC RULES:
- job_description:
  - Write a PROFESSIONAL SUMMARY of the role
  - 10 to 15 lines
  - Combine responsibilities, expectations, and scope
  - No bullet points
  - Plain paragraph text

- required_skills:
  - ONLY technologies, tools, frameworks, or platforms
  - ONE technology per list item
  - No soft skills
  - No sentences or explanations

Return STRICT JSON with these fields:
- job_title
- department
- job_description
- required_skills
- experience_level
- location
- employment_type

JSON SCHEMA:
{{
  "job_title": string,
  "department": string,
  "job_description": string,
  "required_skills": string[],
  "experience_level": string,
  "location": string,
  "employment_type": string
}}

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
            db_job = Job(**job.dict())

            db.add(db_job)
            db.commit()
            db.refresh(db_job)

            return db_job

        except Exception as e:
            db.rollback()
            #raise HTTPException(status_code=500, detail=f"Error creating job: {str(e)}")
            raise ValueError("Failed to create job")


    @staticmethod
    def get_jobs(user_id: int, job_title: str, location: str, search: str | None=None,  page: int = 1, per_page: int = 10, db: Session = None):
        try:
            query = db.query(Job)

            filters = [Job.user_id == user_id]                                 # select * from the job where userid==userid 

            if job_title:   
                filters.append(Job.posting_title.ilike(f"%{job_title}%"))      #  where tile == job tile   

            if location:
                filters.append(
                    or_(
                        Job.city.ilike(f"%{location}%"),
                        Job.state.ilike(f"%{location}%"),
                        Job.country.ilike(f"%{location}%")                     # where location in city or state or country
                    )
                )

            if search:
                search_filter = or_(
                    Job.posting_title.ilike(f"%{search}%"),
                    Job.city.ilike(f"%{search}%"),
                    Job.state.ilike(f"%{search}%"),
                    Job.country.ilike(f"%{search}%")
                )

                filters.append(search_filter)
             
            query = query.filter(and_(*filters))                               # complete query 

            return Paginator.pagination(query,page,per_page)


        except Exception as e:
            #raise HTTPException(status_code=500, detail=f"Error fetching jobs: {str(e)}")
            raise ValueError("Failed to fetch jobs")