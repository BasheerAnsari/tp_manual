from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core_services.app.schemas.recruiter_schema import RecruiterSignupSchema, RecruiterLoginSchema
from core_services.app.core.database import get_db
from core_services.app.services.recruiter_services import recruiter_signup_service, recruiter_signin_service
from core_services.app.shared.helper.error_logger import log_errors
from core_services.app.shared.helper.api_response import api_response


router = APIRouter(prefix="/api/recruiter", tags=["auth"])


# signup
@router.post("/signup", status_code=status.HTTP_201_CREATED)
@log_errors(stage="recruiter_signup_route")
def recruiter_signup(
    data: RecruiterSignupSchema,
    db: Session = Depends(get_db)
):
    recruiter = recruiter_signup_service(db, data)

    return api_response(
        status_code=201,
        successful=True,
        message="Recruiter created successfully",
        data={
            "recruiter_id": recruiter.id
        }
    )

# signin
@router.post("/signin")
@log_errors(stage="recruiter_signin_route")
def recruiter_signin(data: RecruiterLoginSchema, db: Session = Depends(get_db)):
    try:
        result = recruiter_signin_service(data, db)

        return api_response(
            status_code=200,
            successful=True,
            message="Signin successful",
            data=result['user_id']
        )

    except ValueError as ve:
        return api_response(
            status_code=401,
            successful=False,
            message=str(ve),
            data=None
        )