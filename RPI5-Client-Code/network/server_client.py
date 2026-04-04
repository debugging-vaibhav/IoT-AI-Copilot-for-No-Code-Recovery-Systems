"""
Network Server/Client — exposes a Flask API for the backend to call,
and registers this device with the backend on startup.
"""
import threading
import time
import requests
from flask import Flask, request, jsonify
from logger import logger
from config import SERVER_URL, DEVICE_ID, RPI_PORT, SIMULATE_HARDWARE
from control.execution_engine import execute_command
from control.pin_manager import get_all_pin_states
from hardware.sensor_controller import sensor_values

app = Flask(__name__)


# ───────────────────────────────────────────
#  Endpoints the Backend calls on THIS device
# ───────────────────────────────────────────

@app.route("/", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "device_id": DEVICE_ID,
        "simulated": SIMULATE_HARDWARE,
    })


@app.route("/status", methods=["GET"])
def device_status():
    """Returns current pin states and sensor readings."""
    return jsonify({
        "status": "ONLINE",
        "device_id": DEVICE_ID,
        "simulated": SIMULATE_HARDWARE,
        "pin_states": get_all_pin_states(),
        "sensor_readings": {str(k): v for k, v in sensor_values.items()},
    })


@app.route("/execute", methods=["POST"])
def execute():
    """
    Receives a command from the backend and executes it.
    Expected JSON: {"pin": 17, "action": "on"} or
                   {"pin": 12, "action": "servo_control", "angle": 90}
    """
    data = request.get_json(force=True)
    logger.info(f"Received command: {data}")

    result = execute_command(data)
    status_code = 200 if result["success"] else 400
    return jsonify(result), status_code


# ───────────────────────────────────────────
#  Registration with Backend
# ───────────────────────────────────────────

def register_with_backend():
    """Attempts to register this device with the backend server."""
    register_url = f"{SERVER_URL}/api/device/register"
    payload = {
        "device_id": DEVICE_ID,
        "device_url": f"http://{{local_ip}}:{RPI_PORT}",
        "simulated": SIMULATE_HARDWARE,
    }

    # Get local IP for the payload
    import socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
    except Exception:
        local_ip = "127.0.0.1"

    payload["device_url"] = f"http://{local_ip}:{RPI_PORT}"

    while True:
        try:
            resp = requests.post(register_url, json=payload, timeout=5)
            if resp.status_code == 200:
                logger.info(f"✅ Registered with backend at {SERVER_URL} (local IP: {local_ip})")
                return True
            else:
                logger.warning(f"Backend returned {resp.status_code}, retrying in 5s...")
        except requests.exceptions.ConnectionError:
            logger.warning(f"Cannot reach backend at {SERVER_URL}, retrying in 5s...")
        except Exception as e:
            logger.error(f"Registration error: {e}, retrying in 5s...")

        time.sleep(5)


def start_server():
    """Start the Flask server in a background thread."""
    thread = threading.Thread(
        target=lambda: app.run(host="0.0.0.0", port=RPI_PORT, debug=False, use_reloader=False),
        daemon=True,
    )
    thread.start()
    logger.info(f"🚀 RPi Flask server started on port {RPI_PORT}")
    return thread
