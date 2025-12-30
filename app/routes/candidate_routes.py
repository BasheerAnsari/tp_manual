from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from core_services.app.models.candidate_model import Candidate
from core_services.app.schemas.candidate_schema import CandidateSignupSchema, CandidateSigninSchema, CandidateProfileUpdateSchema
from core_services.app.services.candidate_services import candidate_signup_service, candidate_profile_update_service, candidate_signin_service
from core_services.app.core.database import get_db
from core_services.app.shared.helper.api_response import api_response
from core_services.app.shared.helper.error_logger import log_errors


router = APIRouter(prefix="/api/candidate", tags=["candidate"])


# CANDIDATE SIGNUP
@router.post("/signup", status_code=status.HTTP_201_CREATED)
@log_errors(stage="candidate_signup_route")
def candidate_signup(
    data: CandidateSignupSchema,
    db: Session = Depends(get_db)
):
    """
    Candidate signup (used when candidate does not have an account).
    """
    candidate = candidate_signup_service(db, data)

    return api_response(
        status_code=201,
        successful=True,
        message="Candidate account created successfully",
        data={
            "candidate_id": candidate.id,
            "is_profile_completed": candidate.is_profile_completed
        }
    )

# CANDIDATE SIGNIN
@router.post("/signin")
@log_errors(stage="candidate_signin_route")
def candidate_signin(
    data: CandidateSigninSchema,
    db: Session = Depends(get_db)
):
    result = candidate_signin_service(db, data)

    return api_response(
        status_code=200,
        successful=True,
        message="Candidate signin successful",
        data=result
    )

# CANDIDATE PROFILE UPDATE (MANDATORY AFTER SIGNIN)
@router.post("/profile/{candidate_id}")
@log_errors(stage="candidate_profile_update_route")
def update_candidate_profile(
    candidate_id: int,
    data: CandidateProfileUpdateSchema,
    db: Session = Depends(get_db)
):
    """
    Mandatory profile completion step before candidate dashboard.
    """
    candidate_profile_update_service(db, candidate_id, data)

    return api_response(
        status_code=200,
        successful=True,
        message="Candidate profile updated successfully",
        data=None
    )


# # (OPTIONAL) CANDIDATE DASHBOARD ENTRY CHECK
# @router.get("/dashboard/{candidate_id}")
# @log_errors(stage="candidate_dashboard_route")
# def candidate_dashboard_entry(
#     candidate_id: int,
#     db: Session = Depends(get_db)
# ):
#     """
#     Frontend can call this before opening dashboard
#     to ensure profile completion.
#     """
#     from core_services.app.models.candidate_model import Candidate

#     candidate = (
#         db.query(Candidate)
#         .filter(Candidate.id == candidate_id)
#         .first()
#     )

#     if not candidate:
#         return api_response(
#             status_code=404,
#             successful=False,
#             message="Candidate not found",
#             data=None
#         )

#     if not candidate.is_profile_completed:
#         return api_response(
#             status_code=403,
#             successful=False,
#             message="Profile not completed",
#             data={
#                 "redirect": "profile_update"
#             }
#         )

#     return api_response(
#         status_code=200,
#         successful=True,
#         message="Candidate dashboard access granted",
#         data={
#             "candidate_id": candidate.id
#         }
#     )
