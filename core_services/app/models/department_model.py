from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.sql import func
from core_services.app.core.database import Base

class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    department_name = Column(String(255), unique=True, nullable=False)
    #created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
