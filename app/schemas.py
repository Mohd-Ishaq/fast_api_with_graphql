
from pydantic import BaseModel,EmailStr
from typing import Optional




class UserSchema(BaseModel):
    email:EmailStr
    password:str
    is_active:bool


class UserUpdateSchema(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None



class UserOut(BaseModel):
    email:EmailStr
    is_active:bool
    class config:
        orm_mode=True