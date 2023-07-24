from fastapi import FastAPI
import uvicorn
from dotenv import dotenv_values
from src.routers.post_router import router

app = FastAPI()
app.include_router(router)


@app.get("/")
async def health_check():
    return {"message": "Health Check!"}


@app.on_event("startup")
async def startup_event():
    print("startup")


@app.on_event("shutdown")
async def shutdown_event():
    print("shutdown")
    exit(1)


if __name__ == "__main__":
    uvicorn.run(app)
