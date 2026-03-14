from app.db.supabase_client import supabase
from app.models.schemas import ControlLogic
import datetime
import logging

logger = logging.getLogger("uvicorn")

class DatabaseConnectionError(Exception):
    pass

def log_recovery_attempt(status: str, description: str):
    """
    Logs a recovery attempt to the 'recovery_logs' table.
    """
    if supabase is None:
        logger.warning("Supabase not configured. Skipping log_recovery_attempt.")
        raise DatabaseConnectionError("Supabase connection unavailable")
    try:
        data = {
            "status": status,
            "description": description,
            "timestamp": datetime.datetime.now().isoformat()
        }
        supabase.table("recovery_logs").insert(data).execute()
    except Exception as e:
        logger.error(f"Error logging to Supabase: {e}")
        raise DatabaseConnectionError(f"Error logging to Supabase: {str(e)}")

def save_robot_config(logic: ControlLogic):
    """
    Saves a validated configuration to 'robot_config'.
    """
    if supabase is None:
        logger.warning("Supabase not configured. Skipping save_robot_config.")
        raise DatabaseConnectionError("Supabase connection unavailable")
    try:
        data = {
            "sensor": logic.sensor,
            "pin": logic.pin,
            "actuator": logic.action,
            "rule": logic.rule,
            "created_at": datetime.datetime.now().isoformat()
        }
        supabase.table("robot_config").insert(data).execute()
    except Exception as e:
        logger.error(f"Error saving config to Supabase: {e}")
        raise DatabaseConnectionError(f"Error saving config to Supabase: {str(e)}")

def update_system_status(state: str):
    """
    Updates the 'system_status' table.
    """
    if supabase is None:
        logger.warning("Supabase not configured. Skipping update_system_status.")
        raise DatabaseConnectionError("Supabase connection unavailable")
    try:
        data = {
            "state": state,
            "last_updated": datetime.datetime.now().isoformat()
        }
        supabase.table("system_status").insert(data).execute()
    except Exception as e:
        logger.error(f"Error updating system status: {e}")
        raise DatabaseConnectionError(f"Error updating system status: {str(e)}")

def get_recovery_logs():
    """
    Fetches the latest recovery logs.
    """
    if supabase is None:
        logger.warning("Supabase not configured. Returning empty logs.")
        raise DatabaseConnectionError("Supabase connection unavailable")
    try:
        response = supabase.table("recovery_logs").select("*").order("timestamp", desc=True).limit(50).execute()
        return response.data
    except Exception as e:
        logger.error(f"Error fetching logs: {e}")
        raise DatabaseConnectionError(f"Error fetching logs: {str(e)}")

