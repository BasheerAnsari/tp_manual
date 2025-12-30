from fastapi import Request
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from core_services.app.shared.helper.api_response import api_response
from core_services.app.shared.helper.error_logger import error_logger


async def global_exception_handler(request: Request, exc: Exception):
    """
    Catches ALL unhandled exceptions (500 errors)
    across the entire project:
    - routes
    - services
    - background jobs
    - ML services
    """

    # Log the error centrally
    error_logger.add_error(
        stage="global_exception",
        function=request.url.path,
        error_type=type(exc).__name__,
        error_message=str(exc)
    )
    error_logger.save_to_file(context="500_internal_error")

    # Return standardized response
    return api_response(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        successful=False,
        message="Something went wrong. Please try again later.",
        data=None
    )
