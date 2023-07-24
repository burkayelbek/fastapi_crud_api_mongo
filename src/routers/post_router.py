from fastapi import APIRouter, Depends
from src.services.post_service import (
    get_all_posts,
    get_post_by_id,
    add_new_post,
    update_post_full_data,
    update_post_partial_data,
    delete_post_by_id,
)
from src.models import model

router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)


@router.get("/")
async def get_posts():
    posts = get_all_posts()
    return posts


@router.get("/{id}")
async def get_post(id: str):
    post = get_post_by_id(id=id)
    return post


@router.post("/add")
async def add_post(post: model.PostInDb):
    return add_new_post(post=post)


@router.put("/full-update/{id}", response_model=model.PostInDb)
async def update_post_full(id: str, post: model.PostInDb):
    updated_post = update_post_full_data(id=id, updated_item=post)
    return updated_post


@router.patch("/partial-update/{id}", response_model=model.PostInDb)
async def update_post_partial(id: str, updated_item: dict):
    updated_post = update_post_partial_data(id=id, updated_item=updated_item)
    return updated_post


@router.delete("/delete/{id}")
async def delete_post(id: str):
    deleted_post = delete_post_by_id(id=id)
    return deleted_post
