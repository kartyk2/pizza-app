from fastapi import APIRouter

auth_router = APIRouter(prefix= "/auth", tags= ["AUTH"])

@auth_router.get("/")
async def auth_root():
    return {
        "Something Good": f"from {__name__}"
    }
