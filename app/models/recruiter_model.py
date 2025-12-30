from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from sqlalchemy.sql import func
from core_services.app.core.database import Base


class Recruiter(Base):
    __tablename__ = "recruiters"

    id = Column(Integer, primary_key=True, index=True)

    company_name = Column(String(255), nullable=False)
    company_id = Column(String(10), nullable=False)                                 # unique company id need to change "unique=True"

    company_address = Column(Text, nullable=False)
    contact_name = Column(String(255), nullable=False)
    contact_number = Column(String(20), nullable=False)
    # company email
    company_email = Column(String(255), nullable=True)

    # recruter email
    username = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)                                  # have to change the colum name to password_hash

    registration_cert_path = Column(Text, nullable=True)
    gst_cert_path = Column(Text, nullable=True)

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
