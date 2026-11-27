from fastapi import APIRouter
from app.database.connection import client, DATABASE_NAME

router = APIRouter()

@router.get("/health")
def health():
    try:
        client.admin.command("ping", maxTimeMS=3000)

        return {
            "status": "Healthy",
            "backend": "Running",
            "mongodb": "Connected",
            "database": DATABASE_NAME
        }

    except Exception as exc:
        return {
            "status": "Unhealthy",
            "backend": "Running",
            "mongodb": "Disconnected",
            "database": DATABASE_NAME,
            "error": str(exc)
        }