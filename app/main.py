from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.settings import settings
from app.routers import ai


app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "https://smart-haram-monitoring-system.web.app",
        "https://smart-haram-monitoring-system.firebaseapp.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ai.router, prefix=settings.API_PREFIX)


@app.get("/")
def root():
    return {
        "message": "Smart Haram Monitoring System API is running",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
    }
