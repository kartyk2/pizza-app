
from fastapi import APIRouter, Query
from src.schemas.test_schema import *


test_router = APIRouter(prefix= "/TEST", tags= ["TEST"])



@test_router.post("/create")
async def creating_something(item1: class1 | None = None, q_praam1: str= Query(max_length= 5)):

    return {"hhe": "hsbs"}


