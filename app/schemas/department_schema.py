from pydantic import BaseModel, Field

class DepartmentCreateSchema(BaseModel):
    department_name: str = Field(..., min_length=2, description="Department name is required")
