from pydantic import BaseModel, EmailStr
#from typing import Literal

class CommonSigninSchema(BaseModel):
    username: EmailStr
    password: str
    
