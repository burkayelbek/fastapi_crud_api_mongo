from fastapi import FastAPI
from src.config.database import DatabaseConnection
from dotenv import dotenv_values
from models import model
from schemas.schemas import list_posts
from bson import ObjectId

db = DatabaseConnection()
collection = db.get_collection("posts")

app = FastAPI()

@app.get("/posts/list")
async def get_posts():
    posts = list_posts(collection.find())
    return posts

@app.post("/posts")
async def add_post(post: model.Post):
    pass

@app.get("/")
async def health_check():
    return {"message": "Health Check!"}