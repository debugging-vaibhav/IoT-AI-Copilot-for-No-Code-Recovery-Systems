from app.db.supabase_client import supabase
from app.models.schemas import ControlLogic
import datetime
import logging

logger = logging.getLogger("uvicorn")

def log_recovery_attempt(status: str, description: str):
    """
    Logs a recovery attempt to the 'recovery_logs' table.
    """
    if supabase is None:
        logger.warning("Supabase not configured. Skipping log_recovery_attempt.")
        return
    try:
        data = {
            "status": status,
            "description": description,
            "timestamp": datetime.datetime.now().isoformat()
        }
        supabase.table("recovery_logs").insert(data).execute()
    except Exception as e:
        print(f"Error logging to Supabase: {e}")

def save_robot_config(logic: ControlLogic):
    """
    Saves a validated configuration to 'robot_config'.
    """
    if supabase is None:
        logger.warning("Supabase not configured. Skipping save_robot_config.")
        return
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
        print(f"Error saving config to Supabase: {e}")

def update_system_status(state: str):
    """
    Updates the 'system_status' table. 
    Assumes a single row for simple global status, or inserts new one.
    Here we'll insert a new status to keep history, or update the latest if ID=1 is reserved.
    Let's just insert for simplicity log style.
    """
    if supabase is None:
        logger.warning("Supabase not configured. Skipping update_system_status.")
        return
    try:
        data = {
            "state": state,
            "last_updated": datetime.datetime.now().isoformat()
        }
        supabase.table("system_status").insert(data).execute()
    except Exception as e:
        print(f"Error updating system status: {e}")

def get_recovery_logs():
    """
    Fetches the latest recovery logs.
    """
    if supabase is None:
        logger.warning("Supabase not configured. Returning empty logs.")
        return []
    try:
        response = supabase.table("recovery_logs").select("*").order("timestamp", desc=True).limit(50).execute()
        return response.data
    except Exception as e:
        print(f"Error fetching logs: {e}")
        return []

