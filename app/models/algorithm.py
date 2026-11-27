from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class Algorithm(BaseModel):
    algorithm_name: str
    category: str

    description: str

    working_steps: Optional[str] = ""

    time_complexity: Optional[str] = ""

    space_complexity: Optional[str] = ""

    applications: Optional[str] = ""

    advantages: Optional[str] = ""

    disadvantages: Optional[str] = ""

    keywords: List[str] = Field(default_factory=list)

    source: str = "MongoDB"

    created_at: datetime = Field(default_factory=datetime.utcnow)
