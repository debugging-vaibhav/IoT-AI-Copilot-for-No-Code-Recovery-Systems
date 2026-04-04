from app.core.config import settings
import logging
from typing import Optional

logger = logging.getLogger("uvicorn")


def get_supabase():
    url = settings.SUPABASE_URL
    key = settings.SUPABASE_KEY

    if not url or not key or "your_" in url:
        logger.warning("Supabase not configured. Database operations will be skipped.")
        return None

    try:
        from supabase import create_client, Client
        return create_client(url, key)
    except Exception as e:
        logger.warning(f"Could not create Supabase client: {e}")
        return None


supabase = get_supabase()
