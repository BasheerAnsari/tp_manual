from pydantic import BaseModel, Field, EmailStr
from typing import Optional


class FileSchema(BaseModel):
    fileName: str 
    fileBase64: str 


class DocumentsSchema(BaseModel):
    registrationCertificate: Optional[FileSchema] = None
    gstCertificate: Optional[FileSchema] = None


class CompanyInfoSchema(BaseModel):
    companyName: str = Field(..., min_length=3, description="Company name is required")
    companyId: str = Field(..., min_length=10, max_length=10, description="Company PAN is required")
    companyAddress: str = Field(..., min_length=3, description="Company address is required")
    contact_name: str = Field(...,  min_length=3, description="Contact name is required")
    contactNumber: str = Field(..., min_length=10, max_length=10, description="Contact number is required")
    email: Optional[EmailStr] = None


class CredentialsSchema(BaseModel):
    username: str = Field(..., min_length=3, description="Username is required")
    password: str = Field(..., min_length=6, description="Password is required")


class RecruiterSignupSchema(BaseModel):
    companyInfo: CompanyInfoSchema
    credentials: CredentialsSchema
    documents: DocumentsSchema


# recruiter signin schema (login)
class RecruiterLoginSchema(BaseModel):
    username: str = Field(..., description="Username is required")
    password: str = Field(..., description="Password is required")
    