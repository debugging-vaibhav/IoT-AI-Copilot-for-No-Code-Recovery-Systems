from fastapi import APIRouter, Depends, HTTPException
from app.models.schemas import (
    HealthResponse, RobotDescription, ValidationResult, ExecutionRequest,
    ExecutionResponse, ControlLogic, DeviceRegistration, DeviceHeartbeat
)
from app.services.recovery_engine import recovery_system
from app.services.validator import validator
from app.services.iot_interface import iot_interface
from app.services.device_registry import (
    register_device, update_heartbeat, get_all_devices, get_device
)
from app.db.queries import get_recovery_logs, DatabaseConnectionError
from app.core.auth import get_current_user

router = APIRouter()


# ─────────────────────────────────────────────
#  Health & System Status
# ─────────────────────────────────────────────

@router.get("/", response_model=HealthResponse)
def health_check():
    return HealthResponse(status="operational", version="2.0.0")


@router.get("/status")
def system_status():
    """Returns system state including connected devices. No auth for demo."""
    devices = get_all_devices()
    has_online = any(d["status"] == "ONLINE" for d in devices.values()) if devices else False
    return {
        "status": "ACTIVE" if has_online else "NO_DEVICES",
        "hardware": "ONLINE" if has_online else "OFFLINE",
        "connected_devices": len(devices),
        "devices": devices,
    }


# ─────────────────────────────────────────────
#  Device Registration (called by RPi client)
# ─────────────────────────────────────────────

@router.post("/device/register")
def device_register(data: DeviceRegistration):
    """RPi calls this on startup to register itself."""
    register_device(data.device_id, data.device_url, data.simulated)
    return {
        "status": "registered",
        "device_id": data.device_id,
        "message": f"Device {data.device_id} registered at {data.device_url}"
    }


@router.post("/device/heartbeat")
def device_heartbeat(data: DeviceHeartbeat):
    """RPi sends periodic heartbeats to stay alive in the registry."""
    found = update_heartbeat(data.device_id, data.status)
    if not found:
        raise HTTPException(status_code=404, detail=f"Device {data.device_id} not registered")
    return {"status": "ok"}


@router.get("/device/list")
def device_list():
    """List all registered devices and their status."""
    return get_all_devices()


@router.get("/device/{device_id}/status")
def device_live_status(device_id: str):
    """Proxy: fetch live status from a specific RPi device."""
    dev = get_device(device_id)
    if not dev:
        raise HTTPException(status_code=404, detail=f"Device {device_id} not found")

    import requests as req
    try:
        resp = req.get(f"{dev['device_url']}/status", timeout=5)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Cannot reach device: {str(e)}")


# ─────────────────────────────────────────────
#  AI Copilot Endpoints
# ─────────────────────────────────────────────

@router.post("/describe-robot", response_model=ValidationResult)
def describe_robot(input_data: RobotDescription):
    """
    No-auth endpoint for demo.
    Accept description -> Generate Logic -> Validate -> Return result.
    """
    result = recovery_system.process_request(input_data.description)
    return result


@router.post("/generate-logic", response_model=ControlLogic)
def generate_logic_only(input_data: RobotDescription):
    """Generate control logic from description (no validation/apply)."""
    from app.services.ai_copilot import ai_service
    return ai_service.generate_logic(input_data.description)


@router.post("/validate", response_model=ValidationResult)
def validate_logic(logic: ControlLogic):
    """Validate provided logic manually."""
    return validator.validate(logic)


# ─────────────────────────────────────────────
#  Recovery / Execution
# ─────────────────────────────────────────────

@router.post("/recover", response_model=ExecutionResponse)
def apply_recovery(request: ExecutionRequest):
    """Apply validated logic to hardware via the RPi. No auth for demo."""
    result = recovery_system.apply_recovery(request.logic)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    return ExecutionResponse(success=True, message=result["message"])


@router.post("/execute-direct")
def execute_direct(command: dict):
    """
    Direct command execution — sends a raw command to the RPi.
    E.g. {"pin": 17, "action": "on"}
    Useful for the frontend to trigger quick actions.
    """
    success = iot_interface.send_command(
        pin=command.get("pin", 17),
        action=command.get("action", "on")
    )
    if success:
        return {"success": True, "message": f"Command sent to RPi"}
    else:
        raise HTTPException(status_code=502, detail="Could not reach RPi device")


# ─────────────────────────────────────────────
#  Logs
# ─────────────────────────────────────────────

@router.get("/logs")
def get_logs():
    try:
        return get_recovery_logs()
    except DatabaseConnectionError as e:
        return []  # return empty instead of error for demo
