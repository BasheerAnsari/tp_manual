from sqlalchemy.orm import Session
from core_services.app.models.department_model import Department

def create_department_service(db: Session, name: str):
    if db.query(Department).filter(Department.department_name == name).first():
        raise ValueError("Department already exists")

    dept = Department(department_name=name)
    db.add(dept)
    db.commit()
    db.refresh(dept)
    return dept


def get_departments_service(db: Session, search: str | None = None):
    query = db.query(Department)

    if search:
        query = query.filter(Department.department_name.ilike(f"%{search}%"))

    return query.all()
