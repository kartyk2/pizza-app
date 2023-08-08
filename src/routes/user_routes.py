from fastapi import APIRouter


user_router = APIRouter(prefix= "/user")

@user_router.get("/")
async def user_root():
    return{
        __name__: "Router Works Fine"
    }


