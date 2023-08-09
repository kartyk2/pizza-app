from fastapi import FastAPI, Depends
from datetime import datetime

from typing import Annotated
from fastapi.security import OAuth2PasswordBearer

from src.routes.auth_routes import auth_router
from src.routes.user_routes import user_router
from src.routes.test_routes import test_router


app = FastAPI(debug= True)



#including routers
app.include_router(auth_router, prefix="/v1", tags= ["AUTH"])
app.include_router(user_router, prefix="/v1", tags= ["USER"])

app.include_router(test_router)



@app.on_event("startup")
async def start_up():
    print("App Started ------------------------------------", datetime.now())
    return {
    }     




