"""
Device Registry — keeps track of connected Raspberry Pi devices.
In-memory store for the demo. Production would use a database.
"""
import time
import logging

logger = logging.getLogger("uvicorn")

# In-memory registry: device_id -> {device_url, simulated, last_seen, status}
_devices = {}


def register_device(device_id: str, device_url: str, simulated: bool = False):
    _devices[device_id] = {
        "device_url": device_url,
        "simulated": simulated,
        "status": "ONLINE",
        "last_seen": time.time(),
        "registered_at": time.time(),
    }
    logger.info(f"✅ Device registered: {device_id} at {device_url} (simulated={simulated})")


def update_heartbeat(device_id: str, status: str = "ONLINE"):
    if device_id in _devices:
        _devices[device_id]["last_seen"] = time.time()
        _devices[device_id]["status"] = status
        return True
    return False


def get_device(device_id: str) -> dict:
    return _devices.get(device_id, None)


def get_all_devices() -> dict:
    now = time.time()
    result = {}
    for did, info in _devices.items():
        # Mark stale devices (no heartbeat for 30s)
        if now - info["last_seen"] > 30:
            info["status"] = "STALE"
        result[did] = {**info}
    return result


def get_primary_device_url() -> str:
    """Return the URL of the first ONLINE device, or None."""
    for did, info in _devices.items():
        if time.time() - info["last_seen"] < 30:
            return info["device_url"]
    return None


def remove_device(device_id: str):
    _devices.pop(device_id, None)
    logger.info(f"Device removed: {device_id}")
