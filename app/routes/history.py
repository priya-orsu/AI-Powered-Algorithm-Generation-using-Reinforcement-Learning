from fastapi import APIRouter

router = APIRouter(
    prefix="/history",
    tags=["History"]
)

@router.get("/")
def history():
    return {"message": "History API Working"}