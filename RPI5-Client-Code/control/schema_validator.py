"""
Schema Validator — ensures commands are safe before execution.
"""
import json
import os
from logger import logger

SCHEMAS_DIR = os.path.join(os.path.dirname(__file__), "..", "schemas")

# Safe GPIO BCM pins on RPi 3/4/5
SAFE_PINS = {4, 5, 6, 12, 13, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27}
ALLOWED_ACTIONS = {"on", "off", "servo_control", "sensor_stream", "schema_delete"}


def validate_command(command: dict) -> dict:
    """
    Validate a command dict. Returns {"valid": bool, "reason": str}.
    Expected shape: {"action": "on|off|servo_control|...", "pin": int, ...}
    """
    action = command.get("action", "").lower()
    pin = command.get("pin")

    if action not in ALLOWED_ACTIONS:
        return {"valid": False, "reason": f"Unknown action '{action}'. Allowed: {ALLOWED_ACTIONS}"}

    if pin is None:
        return {"valid": False, "reason": "Missing 'pin' field"}

    try:
        pin = int(pin)
    except (ValueError, TypeError):
        return {"valid": False, "reason": f"Pin must be an integer, got '{pin}'"}

    if pin not in SAFE_PINS:
        return {"valid": False, "reason": f"Pin {pin} is not in the safe GPIO list: {sorted(SAFE_PINS)}"}

    if action == "servo_control":
        angle = command.get("angle")
        if angle is None:
            return {"valid": False, "reason": "servo_control requires 'angle' parameter"}
        try:
            angle = float(angle)
        except (ValueError, TypeError):
            return {"valid": False, "reason": f"Angle must be numeric, got '{angle}'"}
        if not (0 <= angle <= 180):
            return {"valid": False, "reason": f"Angle {angle} out of range (0-180)"}

    return {"valid": True, "reason": "Command is safe to execute"}


def load_active_schemas():
    path = os.path.join(SCHEMAS_DIR, "active_schemas.json")
    try:
        with open(path, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_active_schema(pin, schema):
    schemas = load_active_schemas()
    schemas[str(pin)] = schema
    path = os.path.join(SCHEMAS_DIR, "active_schemas.json")
    with open(path, "w") as f:
        json.dump(schemas, f, indent=2)
    logger.info(f"Schema saved for pin {pin}")


def delete_schema(pin):
    schemas = load_active_schemas()
    schemas.pop(str(pin), None)
    path = os.path.join(SCHEMAS_DIR, "active_schemas.json")
    with open(path, "w") as f:
        json.dump(schemas, f, indent=2)
    logger.info(f"Schema deleted for pin {pin}")
