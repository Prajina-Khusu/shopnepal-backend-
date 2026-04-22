from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.get("/test")
async def test():
    return {"message": "Auth router working ✅"}