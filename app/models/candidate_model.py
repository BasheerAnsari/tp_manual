from sqlalchemy import Column, Integer, String, Text, Boolean, TIMESTAMP
from sqlalchemy.sql import func
from core_services.app.core.database import Base


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)

    # ---------- LOGIN CREDENTIALS ----------
    email = Column(String(255), unique=True, nullable=False)
    phone_number = Column(String(20), nullable=False)
    password = Column(String(255), nullable=False)               # have to change the colum name

    # ---------- PROFILE DETAILS ----------
    full_name = Column(String(255), nullable=True)
    years_of_experience = Column(String(20), nullable=True)      # best if it is the Integer
    skills = Column(Text, nullable=True)
    education = Column(Text, nullable=True)

    resume_path = Column(Text, nullable=True)

    # ---------- FLOW CONTROL ----------
    is_profile_completed = Column(Boolean, default=False)

    # ---------- METADATA ----------
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
