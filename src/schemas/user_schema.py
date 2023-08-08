from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    username: str
    email: str
    password: str
    is_active: Optional[bool] = False
    is_admin: Optional[bool] = False


class UserView(BaseModel):
    username: str
    email: str

class UserUpdateSchema(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None