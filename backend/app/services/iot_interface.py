"""
IoT Interface — queues commands for RPi devices to poll.
No longer pushes directly to the device's local IP.
"""
import logging
from app.services.device_registry import (
    enqueue_command,
    get_primary_device_id,
    get_device_cached_status,
)

logger = logging.getLogger("uvicorn")


class IoTInterface:

    def send_command(self, pin: int, action: str, angle: float | None = None) -> bool:
        """Queue a command for the next available online device."""
        device_id = get_primary_device_id()
        if not device_id:
            logger.error("IoT Interface: No online device to queue command for")
            return False

        command = {"pin": pin, "action": action.lower()}
        if angle is not None:
            command["angle"] = angle

        cmd_id = enqueue_command(device_id, command)
        logger.info(f"IoT Interface: Queued command {cmd_id} for {device_id} — pin={pin} action={action}")
        return True

    def get_device_status(self) -> dict:
        """Return the cached status last reported by the device."""
        device_id = get_primary_device_id()
        if not device_id:
            return {"status": "NO_DEVICES", "hardware": "OFFLINE"}

        cached = get_device_cached_status(device_id)
        if cached:
            return cached
        return {"status": "ONLINE", "hardware": "ONLINE", "message": "Awaiting first status report"}


iot_interface = IoTInterface()
