from fastapi import APIRouter
from app.database.connection import client

router = APIRouter()

@router.get("/health")
def health():

    try:
        client.admin.command("ping")

        return {
            "status": "Healthy",
            "backend": "Running",
            "mongodb": "Connected"
        }

    except Exception:

        return {
            "status": "Unhealthy",
            "mongodb": "Disconnected"
        }