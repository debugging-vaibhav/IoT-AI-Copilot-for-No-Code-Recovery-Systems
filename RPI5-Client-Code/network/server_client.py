"""
Network Client — registers with the backend, polls for commands,
and reports results. No local Flask server needed.
"""
import time
import requests
from logger import logger
from config import SERVER_URL, DEVICE_ID, SIMULATE_HARDWARE
from control.execution_engine import execute_command
from control.pin_manager import get_all_pin_states
from hardware.sensor_controller import sensor_values


# ───────────────────────────────────────────
#  Registration with Backend
# ───────────────────────────────────────────

def register_with_backend():
    """Attempts to register this device with the backend server."""
    register_url = f"{SERVER_URL}/api/device/register"
    payload = {
        "device_id": DEVICE_ID,
        "simulated": SIMULATE_HARDWARE,
    }

    while True:
        try:
            resp = requests.post(register_url, json=payload, timeout=5)
            if resp.status_code == 200:
                logger.info(f"Registered with backend at {SERVER_URL}")
                return True
            else:
                logger.warning(f"Backend returned {resp.status_code}, retrying in 5s...")
        except requests.exceptions.ConnectionError:
            logger.warning(f"Cannot reach backend at {SERVER_URL}, retrying in 5s...")
        except Exception as e:
            logger.error(f"Registration error: {e}, retrying in 5s...")

        time.sleep(5)


# ───────────────────────────────────────────
#  Command Polling
# ───────────────────────────────────────────

def poll_commands():
    """Poll the backend for pending commands, execute them, report results."""
    poll_url = f"{SERVER_URL}/api/device/{DEVICE_ID}/commands"
    result_url = f"{SERVER_URL}/api/device/{DEVICE_ID}/commands/result"

    try:
        resp = requests.get(poll_url, timeout=5)
        if resp.status_code != 200:
            logger.debug(f"Poll returned {resp.status_code}")
            return

        data = resp.json()
        commands = data.get("commands", [])
        if not commands:
            return

        logger.info(f"Received {len(commands)} command(s) from backend")
        results = []

        for cmd in commands:
            cmd_id = cmd.get("id", "unknown")
            logger.info(f"Executing command {cmd_id}: {cmd}")

            exec_payload = {
                "pin": cmd.get("pin"),
                "action": cmd.get("action"),
            }
            if cmd.get("angle") is not None:
                exec_payload["angle"] = cmd["angle"]

            result = execute_command(exec_payload)
            results.append({
                "id": cmd_id,
                "success": result.get("success", False),
                "message": result.get("message", ""),
            })

        # Report results back
        if results:
            try:
                requests.post(result_url, json=results, timeout=5)
            except Exception as e:
                logger.warning(f"Failed to report command results: {e}")

    except requests.exceptions.ConnectionError:
        logger.debug("Cannot reach backend for polling")
    except Exception as e:
        logger.error(f"Poll error: {e}")


# ───────────────────────────────────────────
#  Heartbeat (includes device state)
# ───────────────────────────────────────────

def send_heartbeat():
    """Send heartbeat with current device state to the backend."""
    heartbeat_url = f"{SERVER_URL}/api/device/heartbeat"
    payload = {
        "device_id": DEVICE_ID,
        "status": "ONLINE",
        "device_state": {
            "status": "ONLINE",
            "device_id": DEVICE_ID,
            "simulated": SIMULATE_HARDWARE,
            "pin_states": get_all_pin_states(),
            "sensor_readings": {str(k): v for k, v in sensor_values.items()},
        },
    }

    try:
        resp = requests.post(heartbeat_url, json=payload, timeout=5)
        if resp.status_code == 200:
            logger.debug("Heartbeat sent OK")
        else:
            logger.warning(f"Heartbeat returned {resp.status_code}")
    except requests.exceptions.ConnectionError:
        logger.warning("Heartbeat failed — backend unreachable")
    except Exception as e:
        logger.error(f"Heartbeat error: {e}")
