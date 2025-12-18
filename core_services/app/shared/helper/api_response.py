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