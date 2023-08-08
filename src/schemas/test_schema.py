
from pydantic import BaseModel


class class1(BaseModel):
    att1: str | None = None
    att2: int

class class2(BaseModel):
    att1: str
    att2: float | int | str | None = None

    