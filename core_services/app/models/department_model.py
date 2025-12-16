from sqlalchemy import Column, Integer, String
from core_services.app.core.database import Base

class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    department_name = Column(String(255), unique=True, nullable=False)
