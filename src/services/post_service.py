import traceback
from fastapi import status, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
from src.schemas.schemas import list_posts, post_entity
from src.config.database import DatabaseConnection
from datetime import datetime, timedelta


class PostService:
    def __init__(self, db: DatabaseConnection):
        self.collection = db.get_collection("posts")

    def get_all_posts(self):
        posts = list_posts(self.collection.find())
        return posts

    def get_post_by_id(self, id: str):
        if ObjectId.is_valid(id) is False:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                content=jsonable_encoder({"message": f"Invalid id format: {id}. "
                                                                     f"Ex: 11bqxc9dcca5d9d0b6c2ef6f",
                                                          "status": False}))
        post = self.collection.find_one({"_id": ObjectId(id)})
        if post is None:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                                content=jsonable_encoder({"message": "Post does not found",
                                                          "status": False}))
        return post_entity(post)

    def add_new_post(self, post):
        try:
            self.collection.insert_one(dict(post))
            return JSONResponse(content=jsonable_encoder({"message": "Post successfully created", "status": True}),
                                status_code=status.HTTP_201_CREATED)
        except Exception as e:
            traceback.print_exc()
            return JSONResponse(content={"error": "Internal Server Error"},
                                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update_post_full_data(self, id: str, updated_item):
        if ObjectId.is_valid(id) is False:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                content=jsonable_encoder({"message": f"Invalid id format: {id}. "
                                                                     f"Ex: 11bqxc9dcca5d9d0b6c2ef6f",
                                                          "status": False}))

        existing_post = self.collection.find_one({"_id": ObjectId(id)})

        updated_at = existing_post["updated_at"] = datetime.utcnow() + timedelta(hours=3)

        updated_item_dict = updated_item.dict(exclude={"created_at"})

        post = self.collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": {**updated_item_dict, "updated_at": updated_at}}
        )

        if post is None:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                                content=jsonable_encoder({"message": "Post does not found",
                                                          "status": False}))
        updated_post = self.collection.find_one({"_id": ObjectId(id)})

        return post_entity(updated_post)

    def update_post_partial_data(self, id: str, updated_item: dict):
        if ObjectId.is_valid(id) is False:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                content=jsonable_encoder({"message": f"Invalid id format: {id}. "
                                                                     f"Ex: 11bqxc9dcca5d9d0b6c2ef6f",
                                                          "status": False}))

        existing_post = self.collection.find_one({"_id": ObjectId(id)})
        if existing_post is None:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                                content=jsonable_encoder({"message": "Post does not found",
                                                          "status": False}))

        update_fields = {key: value for key, value in updated_item.items() if value is not None}

        update_fields.pop("created_at", None)

        if not update_fields:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content="Cannot find any fields to update")

        invalid_keys = set(update_fields.keys()) - set(existing_post.keys())
        if invalid_keys:
            invalid_keys_str = ", ".join(invalid_keys)
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                content=jsonable_encoder({"message": f"Invalid fields: {invalid_keys_str}. "
                                                                     "These fields are not allowed for update.",
                                                          "status": False}))

        update_fields["updated_at"] = datetime.utcnow() + timedelta(hours=3)
        self.collection.update_one({"_id": ObjectId(id)},
                                   {"$set": update_fields})

        updated_post = self.collection.find_one({"_id": ObjectId(id)})

        return post_entity(updated_post)

    def delete_post_by_id(self, id: str):
        if ObjectId.is_valid(id) is False:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                content=jsonable_encoder({"message": f"Invalid id format: {id}. "
                                                                     f"Ex: 11bqxc9dcca5d9d0b6c2ef6f",
                                                          "status": False}))
        post = self.collection.find_one_and_delete({"_id": ObjectId(id)})
        if post is None:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                                content=jsonable_encoder({"message": "Post not found", "status": False}))
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder({"status": True}))
