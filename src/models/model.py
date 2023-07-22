import uuid

from pydantic import BaseModel, Field, field_validator
from typing import List
from datetime import datetime, timedelta


class PostBase(BaseModel):
    _id: str = Field(default_factory=uuid.uuid4, alias="_id")
    title: str
    short_description: str
    description: str
    tags: List[str]

    class Config:
        from_attributes = True
        populate_by_name = True
        arbitrary_types_allowed = True
        json_schema_extra = {
            "id": "11bqxc9dcca5d9d0b6c2ef6f",
            "title": "Item Model",
            "short_description": "This is an example item description.",
            "description": "This is an example item description.",
            "tags": ["TestTag"]
        }


class PostInDb(PostBase):
    created_at: datetime = Field(default_factory=lambda: datetime.utcnow() + timedelta(hours=3))
    updated_at: datetime = Field(default_factory=lambda: datetime.utcnow() + timedelta(hours=3))
