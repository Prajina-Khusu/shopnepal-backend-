from fastapi import APIRouter

router = APIRouter(prefix="/order", tags=["Order"])

@router.get("/test")
async def test():
    return {"message": "Order router working ✅"}