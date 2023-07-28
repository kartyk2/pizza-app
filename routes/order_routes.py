from fastapi import APIRouter

order_router = APIRouter(prefix= "/order", tags= ["ORDER"])

@order_router.get("/")
async def auth_root():
    return {
        "Something Good": f"from {__name__}"
    }
