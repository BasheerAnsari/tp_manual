from sqlalchemy.orm import Session
#from fastapi import HTTPException

from core_services.app.schemas.common_auth_schema import CommonSigninSchema
from core_services.app.schemas.recruiter_schema import RecruiterLoginSchema
from core_services.app.schemas.candidate_schema import CandidateSigninSchema
from core_services.app.services.recruiter_services import recruiter_signin_service
from core_services.app.services.candidate_services import candidate_signin_service
from core_services.app.core.role_type import validate_role_or_400


def common_signin_service(db: Session, data: CommonSigninSchema, role_type: str):

    response = validate_role_or_400(role_type)
    if response:
        return response

    if role_type == "recruiter":
        result = recruiter_signin_service(
            RecruiterLoginSchema(
                username=data.username,
                password=data.password
            ),
            db
        )

        return {
            "role_type": "recruiter",
            **result
        }

    if role_type == "candidate":
        result = candidate_signin_service(
            db,
            CandidateSigninSchema(
                email=data.username,
                password=data.password
            )
        )

        return {
            "role_type": "candidate",
            **result
        }
    
    # # future roles
    # if role_type in {"admin", "super_admin"}:
    #     raise HTTPException(
    #         status_code=403,
    #         detail="Admin roles not enabled yet"
    #     )

    # Safety fallback (should never hit)
    raise ValueError("Invalid role_type")
