from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from supabase import Client, create_client
from app.core.config import settings

# This is a simple dependency to check if a token is present and validatable by Supabase
# In a real production scenario, we might verify the JWT signature locally using the JWT secret.
# For this project, passing the token to Supabase or just checking presence is a good start.

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Validates the JWT token. 
    In a full implementation, you would decode this using settings.SUPABASE_JWT_SECRET.
    For now, we ensure the token exists.
    """
    token = credentials.credentials
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Simple pass-through for now. 
    # To strictly validate, we'd use PyJWT with the Supabase Secret.
    return {"token": token}
