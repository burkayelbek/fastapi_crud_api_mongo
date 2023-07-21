from fastapi import FastAPI
from src.config.database import DatabaseConnection
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import dotenv_values

app = FastAPI()

# Establish a connection to MongoDB
db_connection = DatabaseConnection()
db_connection.get_connection()
collection = db_connection.get_collection("posts")




@app.get("/")
async def health_check():
    return {"message": "Health Check!"}