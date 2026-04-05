"""
Device Registry — keeps track of connected Raspberry Pi devices.
In-memory store with a command queue so the backend never needs
to push to the RPi's local IP.
"""
import time
import uuid
import logging

logger = logging.getLogger("uvicorn")

# In-memory registry: device_id -> {simulated, last_seen, status, ...}
_devices = {}

# Command queue: device_id -> [pending commands]
_command_queues = {}

# Cached device state: device_id -> latest status payload from heartbeat
_device_status = {}


def register_device(device_id: str, simulated: bool = False):
    _devices[device_id] = {
        "simulated": simulated,
        "status": "ONLINE",
        "last_seen": time.time(),
        "registered_at": time.time(),
    }
    _command_queues.setdefault(device_id, [])
    logger.info(f"Device registered: {device_id} (simulated={simulated})")


def update_heartbeat(device_id: str, status: str = "ONLINE", device_state: dict = None):
    if device_id in _devices:
        _devices[device_id]["last_seen"] = time.time()
        _devices[device_id]["status"] = status
        if device_state:
            _device_status[device_id] = device_state
        return True
    return False


def get_device(device_id: str) -> dict:
    return _devices.get(device_id, None)


def get_all_devices() -> dict:
    now = time.time()
    result = {}
    for did, info in _devices.items():
        if now - info["last_seen"] > 30:
            info["status"] = "STALE"
        result[did] = {**info}
    return result


def get_device_cached_status(device_id: str) -> dict:
    """Return the latest status reported by the device via heartbeat."""
    return _device_status.get(device_id, {})


def get_primary_device_id() -> str | None:
    """Return the device_id of the first ONLINE device, or None."""
    for did, info in _devices.items():
        if time.time() - info["last_seen"] < 30:
            return did
    return None


def enqueue_command(device_id: str, command: dict) -> str:
    """Add a command to the device's pending queue. Returns command ID."""
    cmd_id = uuid.uuid4().hex[:8]
    entry = {"id": cmd_id, **command, "queued_at": time.time()}
    _command_queues.setdefault(device_id, []).append(entry)
    logger.info(f"Command {cmd_id} queued for {device_id}: {command}")
    return cmd_id


def dequeue_commands(device_id: str) -> list:
    """Return and clear all pending commands for a device."""
    commands = _command_queues.get(device_id, [])
    _command_queues[device_id] = []
    return commands


def remove_device(device_id: str):
    _devices.pop(device_id, None)
    _command_queues.pop(device_id, None)
    _device_status.pop(device_id, None)
    logger.info(f"Device removed: {device_id}")
