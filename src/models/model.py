import uuid

from pydantic import BaseModel, Field
from typing import List
from datetime import datetime, timedelta


class Post(BaseModel):
    _id: str = Field(default_factory=uuid.uuid4, alias="_id")
    title: str
    short_description: str
    description: str
    tags: List[str]
    created_at: datetime = Field(default_factory=lambda: datetime.utcnow() + timedelta(hours=3))
    updated_at: datetime = Field(default_factory=lambda: datetime.utcnow() + timedelta(hours=3))

    class Config:
        from_attributes = True
        populate_by_name = True
        arbitrary_types_allowed = True
