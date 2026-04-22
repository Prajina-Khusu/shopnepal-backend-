from fastapi import APIRouter

router = APIRouter(prefix="/review", tags=["review"])

@router.get("/test")
async def test():
    return {"message": "review router working ✅"}