from typing import List
from fastapi import (APIRouter,
                    HTTPException, 
                    status,
                    Depends)

from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from src.connection.connection import get_db
from src.models.models import UserDetails
from passlib.hash import pbkdf2_sha256 as hasing_algorithm
from jwt import encode, decode

from dotenv import load_dotenv
from os import environ

load_dotenv()

SECRET = environ.get("SECRET_KEY")
ALGORITHM= environ.get("ALGORITHM")

from src.schemas.auth_schema import LoginSchema

auth_router = APIRouter(prefix= "/auth")

@auth_router.get("/")
async def auth_root():
    return{
        __name__: "Router Works Fine"
    }

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Endpoint to get an access token (simulated for the example)
@auth_router.post("/token")
async def login(login_details: LoginSchema, db: Session = Depends(get_db)):

    _user = db.query(UserDetails).filter(
        UserDetails.username == login_details.username
    ).first()

    if not _user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"No user with username {login_details.username}")
    
    hash = _user.password
    verify_password = hasing_algorithm.verify(login_details.password, hash= hash)
    # In a real scenario, you would authenticate the user and generate a proper access token
    
    if verify_password:
        data_for_payload = dict(
            sub= login_details.username 
        )

        token = encode(data_for_payload, key= SECRET, algorithm= ALGORITHM)
        return {"access_token": token, "token_type": "bearer"}

    else:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail="Wrong Password")
# Protected endpoint that requires a valid access token
@auth_router.get("/items/")
async def read_items(token: str = Depends(oauth2_scheme)):
    # The token parameter is injected by the dependency oauth2_scheme
    
    payload = decode(token, SECRET, algorithms= [ALGORITHM])
    return {"message": "Access granted", "token": payload}


