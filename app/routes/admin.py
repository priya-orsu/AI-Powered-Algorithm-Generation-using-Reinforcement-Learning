from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.auth.auth import create_access_token
from app.auth.dependencies import verify_token
from app.database.connection import algorithm_collection

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

# --------------------------------------------------
# Login Request Model
# --------------------------------------------------
class LoginRequest(BaseModel):
    username: str
    password: str


# --------------------------------------------------
# Update Algorithm Model
# --------------------------------------------------
class UpdateAlgorithm(BaseModel):
    description: str


# --------------------------------------------------
# Add Algorithm Model
# --------------------------------------------------
class NewAlgorithm(BaseModel):
    algorithm_name: str
    category: str
    description: str
    time_complexity: str
    space_complexity: str


# --------------------------------------------------
# Admin Login
# --------------------------------------------------
@router.post("/login")
def login(data: LoginRequest):

    if data.username == "admin" and data.password == "admin123":

        token = create_access_token(
            {"sub": data.username}
        )

        return {
            "status": "success",
            "access_token": token,
            "token_type": "Bearer"
        }

    return {
        "status": "failed",
        "message": "Invalid Credentials"
    }


# --------------------------------------------------
# Get All Algorithms
# --------------------------------------------------
@router.get("/algorithms")
def get_all_algorithms(
    user=Depends(verify_token)
):

    algorithms = list(
        algorithm_collection.find({}, {"_id": 0})
    )

    return {
        "status": "success",
        "count": len(algorithms),
        "data": algorithms
    }


# --------------------------------------------------
# Add New Algorithm
# --------------------------------------------------
@router.post("/algorithm")
def add_algorithm(
    data: NewAlgorithm,
    user=Depends(verify_token)
):

    # Duplicate Check
    existing = algorithm_collection.find_one(
        {
            "algorithm_name": {
                "$regex": f"^{data.algorithm_name}$",
                "$options": "i"
            }
        }
    )

    if existing:
        return {
            "status": "failed",
            "message": "Algorithm already exists"
        }

    algorithm_collection.insert_one(
        data.model_dump()
    )

    return {
        "status": "success",
        "message": "Algorithm Added Successfully"
    }


# --------------------------------------------------
# Update Algorithm
# --------------------------------------------------
@router.put("/algorithm/{algorithm_name}")
def update_algorithm(
    algorithm_name: str,
    data: UpdateAlgorithm,
    user=Depends(verify_token)
):

    result = algorithm_collection.update_one(
        {
            "algorithm_name": {
                "$regex": f"^{algorithm_name}$",
                "$options": "i"
            }
        },
        {
            "$set": {
                "description": data.description
            }
        }
    )

    if result.matched_count == 0:
        return {
            "status": "failed",
            "message": "Algorithm not found"
        }

    return {
        "status": "success",
        "message": "Algorithm Updated Successfully"
    }


# --------------------------------------------------
# Delete Algorithm
# --------------------------------------------------
@router.delete("/algorithm/{algorithm_name}")
def delete_algorithm(
    algorithm_name: str,
    user=Depends(verify_token)
):

    result = algorithm_collection.delete_one(
        {
            "algorithm_name": {
                "$regex": f"^{algorithm_name}$",
                "$options": "i"
            }
        }
    )

    if result.deleted_count == 0:
        return {
            "status": "failed",
            "message": "Algorithm not found"
        }

    return {
        "status": "success",
        "message": "Algorithm Deleted Successfully"
    }