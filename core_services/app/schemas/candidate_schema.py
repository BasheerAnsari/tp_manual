from pydantic import BaseModel, EmailStr, Field
from typing import Optional
import re


# CANDIDATE SIGNUP
class CandidateSignupSchema(BaseModel):
    email: EmailStr = Field(..., description="Candidate email")
    phone_number: str = Field(
        ..., min_length=10, max_length=10, pattern="^[0-9]{10}$",                                  # have to use the pattren pattern="^[0-9]{10}$"
        description="Candidate phone number"
    )
    password: str = Field(
        ..., min_length=6,
        description="Candidate password"
    )


# CANDIDATE SIGNIN                                                                                 (USED BY COMMON SIGNIN SERVICE)
class CandidateSigninSchema(BaseModel):
    email: EmailStr = Field(..., description="Candidate email")
    password: str = Field(..., description="Candidate password")


# CANDIDATE PROFILE UPDATE (MANDATORY AFTER LOGIN)
class CandidateProfileUpdateSchema(BaseModel):
    full_name: str = Field(..., min_length=3, description="Full name")
    years_of_experience: str = Field(
        ..., description="Total years of experience"
    )
    skills: str = Field(
        ..., description="Comma separated skills"
    )
    education: str = Field(
        ..., description="Education details"
    )

    # Resume upload (base64)
    resumeFileName: str = Field(..., description="Resume file name")
    resumeBase64: str = Field(..., description="Resume file in base64")
