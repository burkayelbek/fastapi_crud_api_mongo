from fastapi import APIRouter, Depends
from src.services.post_service import PostService
from src.models import model
from src.config.database import DatabaseConnection

router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)


def get_post_service(db: DatabaseConnection = Depends(DatabaseConnection)):
    return PostService(db)


@router.get("/")
async def get_posts(service: PostService = Depends(get_post_service)):
    posts = service.get_all_posts()
    return posts


@router.get("/{id}")
async def get_post(id: str, service: PostService = Depends(get_post_service)):
    post = service.get_post_by_id(id=id)
    return post


@router.post("/add")
async def add_post(post: model.PostInDb, service: PostService = Depends(get_post_service)):
    return service.add_new_post(post=post)


@router.put("/full-update/{id}", response_model=model.PostInDb)
async def update_post_full(id: str, post: model.PostInDb, service: PostService = Depends(get_post_service)):
    updated_post = service.update_post_full_data(id=id, updated_item=post)
    return updated_post


@router.patch("/partial-update/{id}", response_model=model.PostInDb)
async def update_post_partial(id: str, updated_item: dict, service: PostService = Depends(get_post_service)):
    updated_post = service.update_post_partial_data(id=id, updated_item=updated_item)
    return updated_post


@router.delete("/delete/{id}")
async def delete_post(id: str,  service: PostService = Depends(get_post_service)):
    deleted_post = service.delete_post_by_id(id=id)
    return deleted_post
