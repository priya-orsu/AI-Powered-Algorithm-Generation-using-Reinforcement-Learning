from pydantic import BaseModel, EmailStr
from datetime import datetime


class User(BaseModel):
    username: str

    email: EmailStr

    password: str

    role: str = "user"

    created_at: datetime = datetime.utcnow()