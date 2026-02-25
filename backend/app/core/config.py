import os
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "IoT AI Copilot Backend"
    API_V1_STR: str = "/api"
    
    # Supabase
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")
    SUPABASE_JWT_SECRET: str = os.getenv("SUPABASE_JWT_SECRET", "")  # For verifying tokens if needed locally

    # OpenAI
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")

    # Hardware
    SIMULATE_HARDWARE: bool = os.getenv("SIMULATE_HARDWARE", "False").lower() == "true"

    class Config:
        env_file = ".env"

settings = Settings()
