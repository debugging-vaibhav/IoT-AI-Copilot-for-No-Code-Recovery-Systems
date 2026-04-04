"""
IoT AI Copilot — Raspberry Pi 5 Edge Client
=============================================
Entry point. Starts the Flask server, registers with the backend,
and runs a heartbeat loop to keep the connection alive.
"""
import time
import threading
import requests
from config import SERVER_URL, DEVICE_ID, RPI_PORT
from logger import logger
from network.server_client import start_server, register_with_backend


def heartbeat_loop():
    """Send periodic heartbeat to backend so it knows we're alive."""
    heartbeat_url = f"{SERVER_URL}/api/device/heartbeat"
    while True:
        try:
            resp = requests.post(heartbeat_url, json={
                "device_id": DEVICE_ID,
                "status": "ONLINE",
            }, timeout=5)
            if resp.status_code == 200:
                logger.debug("Heartbeat sent OK")
            else:
                logger.warning(f"Heartbeat returned {resp.status_code}")
        except requests.exceptions.ConnectionError:
            logger.warning("Heartbeat failed — backend unreachable")
        except Exception as e:
            logger.error(f"Heartbeat error: {e}")

        time.sleep(10)


def main():
    print("=" * 56)
    print("  IoT AI Copilot — Raspberry Pi 5 Edge Client")
    print("=" * 56)
    print(f"  Device ID  : {DEVICE_ID}")
    print(f"  Server URL : {SERVER_URL}")
    print(f"  RPI Port   : {RPI_PORT}")
    print("=" * 56)
    print()

    # 1. Start the Flask server (runs in background thread)
    logger.info("Starting Flask server...")
    start_server()

    # Give Flask a moment to bind
    time.sleep(1)

    # 2. Register with the backend
    logger.info("Registering with backend...")
    reg_thread = threading.Thread(target=register_with_backend, daemon=True)
    reg_thread.start()

    # 3. Start heartbeat loop
    logger.info("Starting heartbeat loop...")
    hb_thread = threading.Thread(target=heartbeat_loop, daemon=True)
    hb_thread.start()

    # 4. Keep main thread alive
    logger.info("RPi client is running. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Shutting down RPi client...")
        print("\nGoodbye!")


if __name__ == "__main__":
    main()
