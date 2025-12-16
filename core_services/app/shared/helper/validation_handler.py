from fastapi.exceptions import RequestValidationError
from core_services.app.shared.helper.api_response import api_response


def validation_exception_handler(request, exc: RequestValidationError):
    error = exc.errors()[0]

    field_path = ".".join(error["loc"][1:])
    error_type = error["type"]

    # ---------------- COMPANY INFO ----------------
    # company name
    if field_path == "companyInfo.companyName":
        if error_type == "string_too_short":
            message = "Company name must be at least 3 characters"
        else:
            message = "Company name should not be empty"

    # company id
    elif field_path == "companyInfo.companyId":
        if error_type in ("string_too_short", "string_too_long"):
            message = "Invalid company id/PAN number"
        else:
            message = "Company ID (PAN) should not be empty"

    # company address
    elif field_path == "companyInfo.companyAddress":
        if error_type == "string_too_short":
            message = "Company address must be at least 3 characters"
        else:
            message = "Company address should not be empty"

    # contact name 
    elif field_path == "companyInfo.contact_name":
        if error_type == "string_too_short":
            message = "Contact name must be at least 3 characters"
        else:
            message = "Contact name should not be empty"

    # contact number
    elif field_path == "companyInfo.contactNumber":
        if error_type == "string_too_short":
            message = "Contact number must be at least 10 digits"
        elif error_type == "string_too_long":
            message = "Contact number must not exceed 10 digits"
        else:
            message = "Contact number should not be empty"

    # ---------------- CREDENTIALS ----------------
    elif field_path == "credentials.username":
        if error_type == "string_too_short":
            message = "Username must be at least 3 characters"
        else:
            message = "Username should not be empty"

    elif field_path == "credentials.password":
        if error_type == "string_too_short":
            message = "Password must be at least 6 characters"
        else:
            message = "Password should not be empty"

    # ---------------- FALLBACK ----------------
    else:
        message = f"{field_path} is invalid"

    return api_response(
        status_code=422,
        successful=False,
        message=message,
        data=None
    )
