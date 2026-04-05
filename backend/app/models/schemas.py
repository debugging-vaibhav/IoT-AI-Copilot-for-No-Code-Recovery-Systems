from pydantic import BaseModel, Field
from typing import Optional, Any, Dict, List


class HealthResponse(BaseModel):
    status: str
    version: str


class RobotDescription(BaseModel):
    description: str = Field(
        ...,
        example="Turn on LED on pin 17 when temperature exceeds 30 degrees"
    )


class ControlLogic(BaseModel):
    sensor: Optional[str] = Field(None, example="temperature")
    pin: int = Field(..., example=17)
    action: str = Field(..., example="ON")
    rule: str = Field(..., example="IF temperature > 30 THEN ON")
    angle: Optional[float] = Field(None, example=90, description="Servo angle 0-180, required for servo_control")


class ValidationResult(BaseModel):
    is_safe: bool
    logic: Optional[ControlLogic]
    message: str


class ExecutionRequest(BaseModel):
    logic: ControlLogic = Field(
        ...,
        example={
            "sensor": "temperature",
            "pin": 17,
            "action": "ON",
            "rule": "IF temperature > 30 THEN ON"
        }
    )


class ExecutionResponse(BaseModel):
    success: bool
    message: str


class SystemStatus(BaseModel):
    state: str = Field(..., example="ACTIVE")
    details: Dict[str, Any] = Field(..., example={"hardware": "ONLINE"})
    last_updated: str = Field(..., example="2026-02-04T19:00:00")


# ── Device Registration & Heartbeat ──

class DeviceRegistration(BaseModel):
    device_id: str = Field(..., example="rpi-5-001")
    simulated: bool = Field(False)


class DeviceHeartbeat(BaseModel):
    device_id: str = Field(..., example="rpi-5-001")
    status: str = Field("ONLINE", example="ONLINE")
    device_state: Optional[Dict[str, Any]] = Field(
        None,
        description="Optional live state: pin_states, sensor_readings, etc.",
    )


# ── Command Queue ──

class CommandResult(BaseModel):
    id: str = Field(..., example="a1b2c3d4")
    success: bool = Field(..., example=True)
    message: str = Field("", example="Executed on action on pin 17")
