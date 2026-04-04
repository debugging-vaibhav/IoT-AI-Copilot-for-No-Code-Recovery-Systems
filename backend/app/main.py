from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
logger = logging.getLogger("uvicorn")
from app.core.config import settings
from app.api import routes

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS — allow React dev server and any origin for demo
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:3001",
    "*"
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
    logger.info("=" * 50)
    logger.info("  IoT AI Copilot Backend — Starting")
    logger.info("=" * 50)
    logger.info(f"  API prefix: {settings.API_V1_STR}")
    logger.info(f"  Docs at: http://0.0.0.0:8000/docs")
    logger.info("=" * 50)


@app.on_event("shutdown")
def shutdown_event():
    logger.info("Shutting down IoT AI Copilot Backend...")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
