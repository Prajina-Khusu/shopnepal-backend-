from fastapi import APIRouter

router = APIRouter(prefix="/Category", tags=["Category"])

@router.get("/test")
async def test():
    return {"message": "Category router working ✅"}