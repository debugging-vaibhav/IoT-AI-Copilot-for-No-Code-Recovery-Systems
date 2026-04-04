from app.db.supabase_client import supabase
from app.models.schemas import ControlLogic
import datetime
import logging

logger = logging.getLogger("uvicorn")


class DatabaseConnectionError(Exception):
    pass


def log_recovery_attempt(status: str, description: str):
    if supabase is None:
        logger.info(f"[LOG] {status}: {description}")
        return
    try:
        data = {
            "status": status,
            "description": description,
            "timestamp": datetime.datetime.now().isoformat()
        }
        supabase.table("recovery_logs").insert(data).execute()
    except Exception as e:
        logger.error(f"Error logging to Supabase: {e}")
        raise DatabaseConnectionError(str(e))


def save_robot_config(logic: ControlLogic):
    if supabase is None:
        logger.info(f"[CONFIG] sensor={logic.sensor} pin={logic.pin} action={logic.action}")
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
        logger.error(f"Error saving config: {e}")
        raise DatabaseConnectionError(str(e))


def update_system_status(state: str):
    if supabase is None:
        logger.info(f"[STATUS] {state}")
        return
    try:
        data = {
            "state": state,
            "last_updated": datetime.datetime.now().isoformat()
        }
        supabase.table("system_status").insert(data).execute()
    except Exception as e:
        logger.error(f"Error updating status: {e}")
        raise DatabaseConnectionError(str(e))


def get_recovery_logs():
    if supabase is None:
        return []
    try:
        response = supabase.table("recovery_logs").select("*").order("timestamp", desc=True).limit(50).execute()
        return response.data
    except Exception as e:
        logger.error(f"Error fetching logs: {e}")
        raise DatabaseConnectionError(str(e))
