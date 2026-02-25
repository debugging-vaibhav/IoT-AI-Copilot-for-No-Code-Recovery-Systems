from fastapi import APIRouter, Depends, HTTPException
from app.models.schemas import (
    HealthResponse, RobotDescription, ValidationResult, ExecutionRequest, 
    ExecutionResponse, ControlLogic
)
from app.services.recovery_engine import recovery_system
from app.services.validator import validator
from app.db.queries import get_recovery_logs
from app.core.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=HealthResponse)
def health_check():
    return HealthResponse(status="operational", version="1.0.0")

@router.get("/status")
def system_status(user=Depends(get_current_user)):
    """
    Returns system state. Protected Endpoint.
    """
    # In a real app we'd fetch actual RPi pin states or DB system_status table
    return {"status": "ACTIVE", "hardware": "ONLINE"}

@router.post("/describe-robot", response_model=ValidationResult)
def describe_robot(input_data: RobotDescription, user=Depends(get_current_user)):
    """
    Step 1 & 2: Accept description -> Generate Logic -> Validate
    """
    result = recovery_system.process_request(input_data.description)
    return result

@router.post("/test-describe-robot", response_model=ValidationResult)
def test_describe_robot(input_data: RobotDescription):
    """
    TEST ENDPOINT (No Auth Required) - Same as describe-robot but without authentication.
    """
    result = recovery_system.process_request(input_data.description)
    return result


@router.post("/generate-logic", response_model=ControlLogic)
def generate_logic_only(input_data: RobotDescription, user=Depends(get_current_user)):
    """
    Direct access to AI generation (without validation/store pipeline implies just viewing)
    """
    # Reuse the service but just key bits
    from app.services.ai_copilot import ai_service
    return ai_service.generate_logic(input_data.description)

@router.post("/validate", response_model=ValidationResult)
def validate_logic(logic: ControlLogic, user=Depends(get_current_user)):
    """
    Validate provided logic manually.
    """
    return validator.validate(logic)

@router.post("/recover", response_model=ExecutionResponse)
def apply_recovery(request: ExecutionRequest, user=Depends(get_current_user)):
    """
    Apply the validated logic to hardware.
    """
    result = recovery_system.apply_recovery(request.logic)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    return ExecutionResponse(success=True, message=result["message"])

@router.get("/logs")
def get_logs(user=Depends(get_current_user)):
    return get_recovery_logs()
