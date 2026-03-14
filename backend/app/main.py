from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

logger = logging.getLogger("uvicorn")
from app.core.config import settings
from app.api import routes

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS Logic
origins = [
    "http://localhost",
    "http://localhost:3000",
    "*"  # Allow all for development/college project ease
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes.router, prefix=settings.API_V1_STR)

@app.on_event("startup")
def startup_event():
    logger.info("Starting up IoT AI Copilot Backend...")

@app.on_event("shutdown")
def shutdown_event():
    logger.info("Shutting down IoT AI Copilot Backend...")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
