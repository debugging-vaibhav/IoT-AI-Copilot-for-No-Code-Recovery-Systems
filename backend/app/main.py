from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import routes
from app.iot.gpio_controller import gpio_manager

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
    # Initialize GPIO
    gpio_manager.setup_board()

@app.on_event("shutdown")
def shutdown_event():
    gpio_manager.cleanup()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
