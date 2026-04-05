"""
IoT AI Copilot — Raspberry Pi 5 Edge Client
=============================================
Entry point. Registers with the backend, then runs a loop
that polls for commands and sends heartbeats.
"""
import time
import threading
from config import SERVER_URL, DEVICE_ID
from logger import logger
from network.server_client import register_with_backend, poll_commands, send_heartbeat

POLL_INTERVAL = 2   # seconds between command polls
HEARTBEAT_INTERVAL = 10  # seconds between heartbeats


def heartbeat_loop():
    """Send periodic heartbeat with device state to the backend."""
    while True:
        send_heartbeat()
        time.sleep(HEARTBEAT_INTERVAL)


def command_poll_loop():
    """Poll the backend for pending commands and execute them."""
    while True:
        poll_commands()
        time.sleep(POLL_INTERVAL)


def main():
    print("=" * 56)
    print("  IoT AI Copilot — Raspberry Pi 5 Edge Client")
    print("=" * 56)
    print(f"  Device ID  : {DEVICE_ID}")
    print(f"  Server URL : {SERVER_URL}")
    print(f"  Mode       : Poll-based (no local server)")
    print("=" * 56)
    print()

    # 1. Register with the backend (blocks until successful)
    logger.info("Registering with backend...")
    reg_thread = threading.Thread(target=register_with_backend, daemon=True)
    reg_thread.start()
    reg_thread.join(timeout=30)

    # 2. Start heartbeat loop
    logger.info("Starting heartbeat loop...")
    hb_thread = threading.Thread(target=heartbeat_loop, daemon=True)
    hb_thread.start()

    # 3. Start command polling loop
    logger.info("Starting command poll loop...")
    poll_thread = threading.Thread(target=command_poll_loop, daemon=True)
    poll_thread.start()

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
