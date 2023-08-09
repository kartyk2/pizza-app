from pydantic import BaseModel, Field
from typing import Optional


class User(BaseModel):
    username: str
    email: str = Field(pattern= r'^[\w\.-]+@[\w\.-]+\.\w+$', examples= ["jhon.doe@email.com"])
    password: str = Field(min_length= 8)
    is_active: bool | None = False
    is_admin: bool | None = False


class UserView(BaseModel):
    username: str
    email: str

class UserUpdateSchema(BaseModel):
    username: str | None = None
    email: str | None = Field(pattern= r'^[\w\.-]+@[\w\.-]+\.\w+$', examples= ["jhon.doe@email.com"], default= None)
    password: str | None = Field(min_length= 8, default= None)
    is_active: bool | None = False
    is_admin: bool | None = False

    