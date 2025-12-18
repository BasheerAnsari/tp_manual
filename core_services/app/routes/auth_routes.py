from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from core_services.app.schemas.common_auth_schema import CommonSigninSchema
from core_services.app.services.common_auth_service import common_signin_service
from core_services.app.core.database import get_db
from core_services.app.shared.helper.api_response import api_response
from core_services.app.shared.helper.error_logger import log_errors

router = APIRouter(prefix="/api", tags=["auth"])


@router.post("/signin")
@log_errors(stage="common_signin_route")
def signin(data: CommonSigninSchema, x_role_type: str = Header(..., alias="X-ROLE-TYPE"), db: Session = Depends(get_db)):

    result = common_signin_service(db, data, x_role_type)

    return api_response(
        status_code=200,
        successful=True,
        message="Signin successful",
        data=result
    )
