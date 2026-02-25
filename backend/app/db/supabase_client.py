from supabase import create_client, Client
from app.core.config import settings
import logging
from typing import Optional

logger = logging.getLogger("uvicorn")

def get_supabase() -> Optional[Client]:
    url = settings.SUPABASE_URL
    key = settings.SUPABASE_KEY
    
    if not url or not key:
        logger.warning("Supabase URL or Key not set. Database operations will fail.")
        return None
    
    return create_client(url, key)

supabase: Optional[Client] = get_supabase()
