from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
from src.models import model
from src.schemas.schemas import list_posts, post_entity
from src.config.database import DatabaseConnection
from datetime import datetime, timedelta

db = DatabaseConnection()
collection = db.get_collection("posts")

router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)


@router.get("/")
async def get_posts():
    posts = list_posts(collection.find())
    return posts


@router.get("/{id}")
async def get_post(id: str):
    if not is_valid_object_id(id):
        return JSONResponse(status_code=400, content=jsonable_encoder({"message": f"Invalid id format: {id}. "
                                                                                  f"It must be a valid ObjectId. "
                                                                                  "Ex: 11bqxc9dcca5d9d0b6c2ef6f",
                                                                       "status": False}))
    post = collection.find_one({"_id": ObjectId(id)})
    if post is None:
        return JSONResponse(status_code=404, content=jsonable_encoder({"message": "Post does not found",
                                                                       "status": False}))
    return post_entity(post)


@router.post("/add")
async def add_post(post: model.PostInDb):
    collection.insert_one(dict(post))


@router.put("/full-update/{id}", response_model=model.PostInDb)
async def update_post_full(id: str, post: model.PostBase):
    if not is_valid_object_id(id):
        return JSONResponse(status_code=400, content=jsonable_encoder({"message": f"Invalid id format: {id}. "
                                                                                  f"It must be a valid ObjectId. "
                                                                                  "Ex: 11bqxc9dcca5d9d0b6c2ef6f",
                                                                       "status": False}))
    updated_at = datetime.utcnow() + timedelta(hours=3)
    updated_post = collection.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": {**dict(post), "updated_at": updated_at}}
    )

    if updated_post is None:
        return JSONResponse(status_code=404, content=jsonable_encoder({"message": "Post does not found",
                                                                       "status": False}))

    # Return the updated post
    return post_entity(updated_post)


@router.patch("/partial-update/{id}", response_model=model.PostInDb)
async def update_post_partial(id: str, post: model.PostInDb):
    # ToDo: partial update does not work. Fix it!
    if not is_valid_object_id(id):
        return JSONResponse(status_code=400, content=jsonable_encoder({"message": f"Invalid id format: {id}. "
                                                                                  f"It must be a valid ObjectId. "
                                                                                  "Ex: 11bqxc9dcca5d9d0b6c2ef6f",
                                                                       "status": False}))

    update_data = dict(post, exclude_unset=True)

    if not update_data:
        return JSONResponse(status_code=400, content="Değiştirilecek bir alan sağlanmadı")

    updated_at = datetime.utcnow() + timedelta(hours=3)

    updated_post = collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": {**dict(update_data), "updated_at": updated_at}},
        return_document=True
    )
    if updated_post is None:
        return JSONResponse(status_code=404, content=jsonable_encoder({"message": "Post does not found",
                                                                       "status": False}))
    # Return the updated post
    return post_entity(updated_post)


@router.delete("/delete/{id}")
async def delete_post(id: str):
    if not is_valid_object_id(id):
        return JSONResponse(status_code=400, content=jsonable_encoder({"message": f"Invalid id format: {id}. "
                                                                                  f"It must be a valid ObjectId. "
                                                                                  "Ex: 11bqxc9dcca5d9d0b6c2ef6f",
                                                                       "status": False}))
    post = collection.find_one_and_delete({"_id": ObjectId(id)})
    if post is None:
        return JSONResponse(status_code=200, content=jsonable_encoder({"message": "Post not found", "status": False}))
    return JSONResponse(status_code=200, content=jsonable_encoder({"status": True}))


def is_valid_object_id(value):
    try:
        ObjectId(value)
        return True
    except Exception:
        return False
