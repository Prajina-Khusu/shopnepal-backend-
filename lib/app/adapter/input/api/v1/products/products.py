from fastapi import APIRouter

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/test")
async def test():
    return {"message": "Products router working ✅"}