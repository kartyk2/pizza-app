from typing import List
from fastapi import APIRouter, HTTPException, status
from src.schemas.user_schema import User, UserView, UserUpdateSchema
from sqlalchemy.orm import Session
from sqlalchemy import update
from fastapi import Depends
from src.connection.connection import get_db
from src.models.models import UserDetails
import re
import uuid
from passlib.hash import pbkdf2_sha256 as hasing_algorithm

user_router = APIRouter(prefix= "/user")

@user_router.get("/")
async def user_root():
    return{
        __name__: "Router Works Fine"
    }


class UserActions:
    def __init__(self, db: Session) -> None:
        self.db = db
    
    def add_to_db(self, mapping_object: UserDetails):
        try:
            self.db.add(mapping_object)
            self.db.commit()
            return {
                "Status": "Added Sucessfully"
            }
        except Exception as error:
            raise error
        
    
    def json_to_mapping(self, object: User, hashed_password: str|bytes):
        try:
            object_JSON = object.model_dump()
            object_JSON.update(password = hashed_password)

            return UserDetails(**object_JSON)

        except Exception as error:
            raise error
    

    def check_if_already_exists(self, user:User):
        try:
            query_user = self.db.query(UserDetails).filter(UserDetails.email==user.email).first()
            if query_user:
                raise HTTPException(status_code= status.HTTP_409_CONFLICT, detail= "Duplicate Entry, email exists")
            
            query_user = self.db.query(UserDetails).filter(UserDetails.username==user.username).first()
            if query_user:
                raise HTTPException(status_code= status.HTTP_409_CONFLICT, detail= "Duplicate Entry, username exists")
        
        except Exception as error:
            raise error


    def find_one_entry(self, id: uuid.UUID):
        try:
            user = self.db.query(UserDetails).filter(UserDetails.id == id).first()
            if not user:
                raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="ID does not exist")
            
            return user
        
        except HTTPException as error:
            raise error

    def update_schema_to_JSON(self, schemaObject: UserUpdateSchema):
        # Build the update statement dynamically based on provided fields
        try:
            stmt_data = {}
            for field, value in schemaObject.model_dump().items():
                if value is not None:
                    stmt_data[field] = value

            password = stmt_data.get("password", None)

            if password:
                hashed = hasing_algorithm.hash(password)
                stmt_data.update(password = hashed)
            return stmt_data

        except Exception as error:
            raise error  
          
""" 

# ------------------------- ROUTES ---------------------------------------


"""
        

@user_router.post("/create_user", response_model= UserView)
async def create_user(user: User, db: Session = Depends(get_db)):
    try:
        _user = UserActions(db= db)
        
        _user.check_if_already_exists(user)

        hashed = hasing_algorithm.hash(user.password)

        db_user = _user.json_to_mapping(user, hashed_password = hashed)
        result = _user.add_to_db(db_user)


        return db_user
    
    except Exception as error:
        raise error



@user_router.get("/all_users")
async def fetch_users(db: Session = Depends(get_db)):
    try:
        _user = UserActions(db= db)
    
        result = db.query(UserDetails).all()
        return result
    except Exception as error:
        raise error


@user_router.get("/user/{id}")
async def fetch_user(id: uuid.UUID, db: Session = Depends(get_db)):
    try:
        _user = UserActions(db= db)
    
        result = _user.find_one_entry(id= id)
        return result
    except Exception as error:
        raise error



@user_router.delete("/delete_user/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: uuid.UUID, db: Session = Depends(get_db)):

    _user = db.query(UserDetails).filter(UserDetails.id == user_id).first()
    if not _user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Such user Exists")

    try:
        db.delete(_user)
        db.commit()
    except Exception as error:
        db.rollback()
        raise error


from sqlalchemy import update

@user_router.put("/update_user/{id}", status_code=status.HTTP_202_ACCEPTED)
async def update_user(id: uuid.UUID, updateDetails: UserUpdateSchema, db: Session = Depends(get_db)):
    try:
        _user = UserActions(db=db)
        db_user = _user.find_one_entry(id=id)

        stmt_data = _user.update_schema_to_JSON(updateDetails)
        # Build the update statement dynamically based on provided fields

        stmt = (
            update(UserDetails)
            .where(UserDetails.id == id)
            .values(stmt_data)
        )

        db.execute(stmt)
        db.commit()
        
    except HTTPException as error:
        db.rollback()
        raise error

