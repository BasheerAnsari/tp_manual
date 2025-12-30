from fastapi import APIRouter, Header, Depends, Query
from sqlalchemy.orm import Session

from core_services.app.core.database import get_db
from core_services.app.core.role_type import validate_role_or_400
from core_services.app.services.dashboard_service import get_recruiter_dashboard_service
from core_services.app.shared.helper.api_response import api_response
from core_services.app.shared.helper.error_logger import log_errors

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/recruiter")
def get_dashboard(x_role_type: str = Header(..., alias="X-ROLE-TYPE")):

    response = validate_role_or_400(x_role_type)
    if response:
        return response

    if x_role_type != "recruiter":
        return api_response(403, False, "Access denied", None)

    data = get_recruiter_dashboard_service()

    return api_response(
        status_code=200,
        successful=True,
        message="Recruiter dashboard fetched successfully",
        data=data
    )