from pydantic import BaseModel, Field
from typing import List
from datetime import datetime, timedelta


class Post:
    title: str
    short_description: str
    description: str
    tags: List[str]
    created_at: datetime = Field(default_factory=lambda: datetime.utcnow() + timedelta(hours=3))
    updated_at: datetime = Field(default_factory=lambda: datetime.utcnow() + timedelta(hours=3))
