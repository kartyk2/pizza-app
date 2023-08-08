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




oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Endpoint to get an access token (simulated for the example)
@app.post("/token")
async def get_token():
    # In a real scenario, you would authenticate the user and generate a proper access token
    token = "That's Your Token"
    return {"access_token": token, "token_type": "bearer"}


# Protected endpoint that requires a valid access token
@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    # The token parameter is injected by the dependency oauth2_scheme
    return {"message": "Access granted", "token": token}


