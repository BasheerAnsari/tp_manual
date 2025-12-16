from fastapi import APIRouter
from core_services.app.services.dashboard_service import get_recruiter_dashboard_service
from core_services.app.shared.helper.api_response import api_response

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/recruiter")
def get_dashboard():
    data = get_recruiter_dashboard_service()

    return api_response(
        status_code=200,
        successful=True,
        message="Recruiter dashboard fetched successfully",
        data=data
    )