import os
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    PROJECT_NAME: str = "IoT AI Copilot Backend"
    API_V1_STR: str = "/api"

    # Supabase (optional for demo)
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")
    SUPABASE_JWT_SECRET: str = os.getenv("SUPABASE_JWT_SECRET", "")

    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")

    # Default RPi URL — overridden when a device registers
    IOT_SERVICE_URL: str = os.getenv("IOT_SERVICE_URL", "http://raspberrypi:5000")

    class Config:
        env_file = ".env"


settings = Settings()
