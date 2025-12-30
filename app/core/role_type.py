import json
from pathlib import Path
from starlette.status import HTTP_400_BAD_REQUEST

from core_services.app.shared.helper.api_response import api_response

ROLE_FILE = Path(__file__).parent / "role_type.json"

with open(ROLE_FILE, "r") as f:
    ROLE_TYPES = json.load(f)


def is_valid_role(role_type: str) -> bool:
    return role_type in ROLE_TYPES


def validate_role_or_400(role_type: str):
    if not is_valid_role(role_type):
        return api_response(
            status_code=HTTP_400_BAD_REQUEST,
            successful=False,
            message="Invalid role type",
            data={
                "allowed_roles": list(ROLE_TYPES.keys())
            }
        )
