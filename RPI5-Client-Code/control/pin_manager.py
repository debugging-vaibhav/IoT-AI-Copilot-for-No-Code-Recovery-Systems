"""
Pin Manager — tracks which pins are in use and their current state.
"""
import json
import os
from logger import logger

SCHEMAS_DIR = os.path.join(os.path.dirname(__file__), "..", "schemas")
PIN_STATE_FILE = os.path.join(SCHEMAS_DIR, "pin_state.json")


def _load_state():
    try:
        with open(PIN_STATE_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _save_state(state):
    os.makedirs(os.path.dirname(PIN_STATE_FILE), exist_ok=True)
    with open(PIN_STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def set_pin_state(pin, action, details=None):
    state = _load_state()
    state[str(pin)] = {
        "action": action,
        "details": details or {},
    }
    _save_state(state)
    logger.info(f"Pin {pin} state updated: {action}")


def get_pin_state(pin):
    state = _load_state()
    return state.get(str(pin), None)


def get_all_pin_states():
    return _load_state()


def release_pin(pin):
    state = _load_state()
    state.pop(str(pin), None)
    _save_state(state)
    logger.info(f"Pin {pin} released")
