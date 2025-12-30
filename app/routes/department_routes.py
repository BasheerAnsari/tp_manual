from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core_services.app.core.database import get_db
from core_services.app.schemas.department_schema import DepartmentCreateSchema
from core_services.app.services.department_service import create_department_service, get_departments_service
from core_services.app.shared.helper.api_response import api_response

router = APIRouter(prefix="/api/departments", tags=["departments"])


# CREATE DEPARTMENT
@router.post("")
def create_department(
    payload: DepartmentCreateSchema,
    db: Session = Depends(get_db)
):
    
    dept = create_department_service(db, payload.department_name)

    return api_response(
        status_code=201,
        successful=True,
        message="Department created successfully",
        data={
            "id": dept.id,
            "department_name": dept.department_name
        }
    )

    

# GET ALL DEPARTMENTS 
@router.get("")
def get_departments(
    db: Session = Depends(get_db)
):
    depts = get_departments_service(db)

    return api_response(
        status_code=200,
        successful=True,
        message="Departments fetched successfully",
        data=[
            {
                "id": d.id,
                "department_name": d.department_name
            }
            for d in depts
        ]
    )
