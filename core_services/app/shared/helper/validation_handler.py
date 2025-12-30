# from fastapi.exceptions import RequestValidationError
# from core_services.app.shared.helper.api_response import api_response


# def validation_exception_handler(request, exc: RequestValidationError):
#     error = exc.errors()[0]

#     field_path = ".".join(error["loc"][1:])
#     error_type = error["type"]

#     # ---------------- COMPANY INFO ----------------
#     # company name
#     if field_path == "companyInfo.companyName":
#         if error_type == "string_too_short":
#             message = "Company name must be at least 3 characters"
#         else:
#             message = "Company name should not be empty"

#     # company id
#     elif field_path == "companyInfo.companyId":
#         if error_type in ("string_too_short", "string_too_long"):
#             message = "Invalid company id/PAN number"
#         else:
#             message = "Company ID (PAN) should not be empty"

#     # company address
#     elif field_path == "companyInfo.companyAddress":
#         if error_type == "string_too_short":
#             message = "Company address must be at least 3 characters"
#         else:
#             message = "Company address should not be empty"

#     # contact name 
#     elif field_path == "companyInfo.contact_name":
#         if error_type == "string_too_short":
#             message = "Contact name must be at least 3 characters"
#         else:
#             message = "Contact name should not be empty"

#     # contact number
#     elif field_path == "companyInfo.contactNumber":
#         if error_type == "string_too_short":
#             message = "Contact number must be at least 10 digits"
#         elif error_type == "string_too_long":
#             message = "Contact number must not exceed 10 digits"
#         else:
#             message = "Contact number should not be empty"

#     # ---------------- CREDENTIALS ----------------
#     elif field_path == "credentials.username":
#         if error_type == "string_too_short":
#             message = "Username must be at least 3 characters"
#         else:
#             message = "Username should not be empty"

#     elif field_path == "credentials.password":
#         if error_type == "string_too_short":
#             message = "Password must be at least 6 characters"
#         else:
#             message = "Password should not be empty"

#     # ---------------- FALLBACK ----------------
#     else:
#         message = f"{field_path} is invalid"

#     return api_response(
#         status_code=422,
#         successful=False,
#         message=message,
#         data=None
#     )

from fastapi.exceptions import RequestValidationError
from fastapi import Request
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from core_services.app.shared.helper.api_response import api_response


def humanize_field(field_path: list) -> str:
    """
    Converts nested field paths into readable names.
    Example:
    ["body", "companyInfo", "company_id"] -> "Company Info Company Id"
    """
    fields = [str(f) for f in field_path if f not in ("body", "query", "path")]
    return " ".join(fields).replace("_", " ").title()


def business_message(error: dict) -> str:
    """
    Generate business-friendly error messages
    from Pydantic validation error.
    """
    error_type = error.get("type", "")
    ctx = error.get("ctx", {}) or {}                              # ctx alwasy dictionary
    field_name = humanize_field(error.get("loc", []))

    # ---------------- REQUIRED ----------------
    if "missing" in error_type:
        return f"{field_name} is required"

    # ---------------- STRING LENGTH ----------------
    if error_type == "string_too_short":
        min_len = ctx.get("min_length")
        return (
            f"{field_name} must be at least {min_len} characters"
            if min_len else f"{field_name} cannot be empty"
        )

    if error_type == "string_too_long":
        max_len = ctx.get("max_length")
        return (
            f"{field_name} must not exceed {max_len} characters"
            if max_len else f"{field_name} is too long"
        )

    # ---------------- NUMERIC LIMITS ----------------
    if error_type in ("greater_than", "greater_than_equal"):
        limit = ctx.get("gt") or ctx.get("ge")
        return f"{field_name} must be greater than {limit}"

    if error_type in ("less_than", "less_than_equal"):
        limit = ctx.get("lt") or ctx.get("le")
        return f"{field_name} must be less than {limit}"

    # ---------------- TYPE ERRORS ----------------
    if "int_parsing" in error_type:
        return f"{field_name} must be a number"

    if "float_parsing" in error_type:
        return f"{field_name} must be a valid number"

    if "list_type" in error_type:
        return f"{field_name} must be a list"

    # ---------------- ENUM / LITERAL ----------------
    if error_type == "literal_error":
        allowed = ctx.get("expected")
        if allowed:
            return f"{field_name} must be one of {allowed}"
        return f"Invalid value for {field_name}"

    # ---------------- REGEX ----------------
    if error_type == "string_pattern_mismatch":
        return f"{field_name} format is invalid"

    # ---------------- FALLBACK ----------------
    return f"Invalid {field_name}"


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    """
    Global validation handler used across:
    - Auth
    - Jobs
    - Interviews
    - Dashboards
    - ML services
    - Background jobs
    """
    errors = [
        {
            "field": humanize_field(err.get("loc", [])),
            "message": business_message(err)
        }
        for err in exc.errors()
    ]

    return api_response(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        successful=False,
        message="Invalid request data",
        data=errors
    )
