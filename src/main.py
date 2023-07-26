import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from dotenv import dotenv_values
from src.routers import post_router

app = FastAPI()
app.include_router(post_router.router)


@app.get("/", include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url='/docs')


@app.get("/health-check", tags=["Health Check"])
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
