from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

def api_response(status_code: int, successful: bool, message: str, data=None):
    return JSONResponse(
        status_code=status_code,
        content={
            "status_code": status_code,
            "successful": successful,
            "message": message,
            "data": jsonable_encoder(data)
        }
    )

# from fastapi.responses import JSONResponse
# from fastapi.encoders import jsonable_encoder
# from typing import Optional, Dict, Any


# def api_response(
#     status_code: int,
#     successful: bool,
#     message: str,
#     data: Any = None,
#     pagination: Optional[Dict[str, int]] = None
# ):
#     """
#     Standard API response.
#     Pagination is included ONLY when provided.
#     """

#     content = {
#         "status_code": status_code,
#         "successful": successful,
#         "message": message
#     }

#     # Add pagination block BEFORE data (exact order you want)
#     if pagination:
#         content["pagination"] = {
#             "page": pagination.get("page"),
#             "per_page": pagination.get("per_page"),
#             "total": pagination.get("total"),
#             "total_pages": pagination.get("total_pages")
#         }

#     # Data always comes last
#     content["data"] = jsonable_encoder(data)

#     return JSONResponse(
#         status_code=status_code,
#         content=content
#     )
