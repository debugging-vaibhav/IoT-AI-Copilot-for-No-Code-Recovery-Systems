from __future__ import annotations
from pydantic import BaseModel, Field


class ProcessRequest(BaseModel):
    description: str = Field(..., min_length=1, description="Natural-language instruction from the user")
    device_context: dict | None = Field(default=None, description="Optional current device state (pin states, sensor readings)")


class HardwareCommand(BaseModel):
    pin: int
    action: str  # on | off | servo_control | sensor_stream | schema_delete
    angle: float | None = None  # required only for servo_control


class ProcessResponse(BaseModel):
    is_safe: bool
    message: str
    commands: list[HardwareCommand]
    reasoning: str = ""


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
