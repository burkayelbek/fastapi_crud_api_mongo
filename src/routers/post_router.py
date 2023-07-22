from fastapi import APIRouter
from bson import ObjectId
from src.models import model
from src.schemas.schemas import list_posts
from src.config.database import DatabaseConnection

db = DatabaseConnection()
collection = db.get_collection("posts")

router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)


@router.get("/list")
async def get_posts():
    posts = list_posts(collection.find())
    return posts


@router.post("/")
async def add_post(post: model.Post) -> post_response_entity:
    collection.insert_one(dict(post))

@router.put("/{id}")
async def add_post(id: str, post: model.Post) -> post_response_entity:
    collection.find_one_and_update({"_id": ObjectId(id)}, {"$set": dict(post)})

@router.delete("/{id}")
async def add_post(id: str):
    collection.find_one_and_delete({"_id": ObjectId(id)})
