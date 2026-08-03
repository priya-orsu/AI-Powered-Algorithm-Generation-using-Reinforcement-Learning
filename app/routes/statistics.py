from fastapi import APIRouter

router = APIRouter(
    prefix="/statistics",
    tags=["Statistics"]
)

@router.get("/")
def statistics():
    return {"message": "Statistics API Working"}