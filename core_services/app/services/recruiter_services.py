import os
import uuid
import base64
from sqlalchemy.orm import Session
from passlib.hash import bcrypt

from core_services.app.models.recruiter_model import Recruiter
from core_services.app.schemas.recruiter_schema import RecruiterLoginSchema
from core_services.app.shared.helper.error_logger import log_errors

from fastapi import HTTPException, status


UPLOAD_DIR = "uploads/recruiter_docs"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def _save_file(file_obj):
    """
    Saves base64 file to uploads folder and returns file path
    """
    file_name = f"{uuid.uuid4()}_{file_obj.fileName}"
    file_path = os.path.join(UPLOAD_DIR, file_name)

    file_bytes = base64.b64decode(file_obj.fileBase64)
    with open(file_path, "wb") as f:
        f.write(file_bytes)

    return file_path


# signup service
@log_errors(stage="recruiter_signup_service")
def recruiter_signup_service(db: Session, data):

     # Check duplicate username
    if db.query(Recruiter).filter(
        Recruiter.username == data.credentials.username
    ).first():
        raise ValueError("Username already exists")

    # password hashing(72 bytes)
    raw_password = data.credentials.password
    safe_password = raw_password.encode("utf-8")[:72].decode("utf-8", errors="ignore")
    hashed_password = bcrypt.hash(safe_password)

    # Optional documents
    registration_path = None
    gst_path = None

    if data.documents and data.documents.registrationCertificate:
        registration_path = _save_file(
            data.documents.registrationCertificate
        )

    if data.documents and data.documents.gstCertificate:
        gst_path = _save_file(
            data.documents.gstCertificate
        )

    try:
        new_recruiter = Recruiter(
            company_name=data.companyInfo.companyName,
            company_id=data.companyInfo.companyId,
            company_address=data.companyInfo.companyAddress,
            contact_name=data.companyInfo.contact_name,
            contact_number=data.companyInfo.contactNumber,
            company_email=data.companyInfo.email,
            username=data.credentials.username,
            password=hashed_password,
            registration_cert_path=registration_path,
            gst_cert_path=gst_path
        )

        db.add(new_recruiter)
        db.commit()
        db.refresh(new_recruiter)

        return new_recruiter
    
    except Exception:
        db.rollback()
        raise ValueError("Failed to create recruiter account")   


# signin service
@log_errors(stage="recruiter_signin_service")
def recruiter_signin_service(data: RecruiterLoginSchema, db: Session):

    user = db.query(Recruiter).filter(
        Recruiter.username == data.username
    ).first()

    if not user:
        raise ValueError("Invalid username or password")

    # BCRYPT SAFE CHECK
    raw_password = data.password
    safe_password = raw_password.encode("utf-8")[:72].decode("utf-8", errors="ignore")

    if not bcrypt.verify(safe_password, user.password):
        raise ValueError("Invalid username or password")

    return {
        "user_id": user.id,
        "username": user.username
    }