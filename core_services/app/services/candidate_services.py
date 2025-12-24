import os
import uuid
import base64
from sqlalchemy.orm import Session
from passlib.hash import bcrypt
#from fastapi import HTTPException, status

from core_services.app.models.candidate_model import Candidate
from core_services.app.schemas.candidate_schema import CandidateSignupSchema, CandidateSigninSchema, CandidateProfileUpdateSchema
from core_services.app.shared.helper.error_logger import log_errors


# FILE STORAGE CONFIG
UPLOAD_DIR = "uploads/candidate_docs"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def _save_resume(file_name: str, file_base64: str) -> str:
    """
    Save candidate resume to uploads/candidate_docs
    and return file path
    """
    
    try:
        unique_name = f"{uuid.uuid4()}_{file_name}"
        file_path = os.path.join(UPLOAD_DIR, unique_name)
        file_bytes = base64.b64decode(file_base64)

        with open(file_path, "wb") as f:
            f.write(file_bytes)

        return file_path
    except Exception:
        raise ValueError("Failed to save resume file")



# CANDIDATE SIGNUP
@log_errors(stage="candidate_signup_service")
def candidate_signup_service(db: Session, data: CandidateSignupSchema):
    # Check duplicate email
    if db.query(Candidate).filter(Candidate.email == data.email).first():
        raise ValueError("Email already registered")

    # bcrypt safety (72 bytes max)
    safe_password = data.password.encode("utf-8")[:72].decode(
        "utf-8", errors="ignore"
    )
    hashed_password = bcrypt.hash(safe_password)

    candidate = Candidate(
        email=data.email,
        phone_number=data.phone_number,
        password=hashed_password,
        is_profile_completed=False
    )

    try:
        db.add(candidate)
        db.commit()
        db.refresh(candidate)
        return candidate

    except Exception:
        db.rollback()
        raise ValueError("Failed to create candidate account")


# CANDIDATE SIGNIN (USED BY COMMON AUTH SERVICE)
@log_errors(stage="candidate_signin_service")
def candidate_signin_service(db: Session, data: CandidateSigninSchema):
    candidate = (
        db.query(Candidate)
        .filter(Candidate.email == data.email)
        .first()
    )

    if not candidate:
        raise ValueError("Invalid email or password")

    safe_password = data.password.encode("utf-8")[:72].decode("utf-8", errors="ignore")

    if not bcrypt.verify(safe_password, candidate.password):
        raise ValueError("Invalid email or password")

    return {
        "candidate_id": candidate.id,
        "is_profile_completed": candidate.is_profile_completed
    }

# CANDIDATE PROFILE UPDATE (MANDATORY STEP)
@log_errors(stage="candidate_profile_update_service")
def candidate_profile_update_service(
    db: Session,
    candidate_id: int,
    data: CandidateProfileUpdateSchema
):
    candidate = (
        db.query(Candidate)
        .filter(Candidate.id == candidate_id)
        .first()
    )

    if not candidate:
        raise ValueError("Candidate not found")

    # MANDATORY RESUME VALIDATION
    if not data.resumeBase64 or data.resumeBase64.strip().lower() == "string":
        raise ValueError("Resume is mandatory and must be a valid file")

    if not data.resumeFileName:
        raise ValueError("Resume file name is required")

    # Save resume only after validation
    resume_path = _save_resume(
        data.resumeFileName,
        data.resumeBase64
    )

    try:
        candidate.full_name = data.full_name
        candidate.years_of_experience = data.years_of_experience
        candidate.skills = data.skills
        candidate.education = data.education
        candidate.resume_path = resume_path
        candidate.is_profile_completed = True

        db.commit()
        return candidate

    except Exception:
        db.rollback()
        raise ValueError("Failed to update candidate profile")
