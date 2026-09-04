from fastapi import FastAPI

from backend.routes.calorie import router as calorie_router
from backend.routes.chat import router as chat_router
from backend.routes.food import router as food_router


@app.get("/")
def read_root():
    return {"Python": "on Vercel"}

app = FastAPI(
    title="Indian Diet AI",
    description="LLM and RAG based Indian Food Calorie Calculator",
    version="1.0.0"
)

app.include_router(calorie_router)
app.include_router(chat_router)
app.include_router(food_router)


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }

@app.get("/")
def root():

    return {
        "message": "Indian Diet AI API is running",
        "status": "success"
    }


