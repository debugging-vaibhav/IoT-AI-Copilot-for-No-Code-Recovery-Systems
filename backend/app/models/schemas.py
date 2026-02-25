from pydantic import BaseModel, Field
from typing import Optional, Any, Dict

class HealthResponse(BaseModel):
    status: str
    version: str

class RobotDescription(BaseModel):
    description: str = Field(
        ...,
        example="Turn on LED on pin 17 when temperature exceeds 30 degrees"
    )

class ControlLogic(BaseModel):
    sensor: str = Field(..., example="temperature")
    pin: int = Field(..., example=17)
    action: str = Field(..., example="ON")
    rule: str = Field(..., example="IF temperature > 30 THEN ON")

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
