from fastapi import APIRouter

router = APIRouter(prefix="/cart", tags=["Cart"])

@router.get("/test")
async def test():
    return {"message": "Cart router working ✅"}