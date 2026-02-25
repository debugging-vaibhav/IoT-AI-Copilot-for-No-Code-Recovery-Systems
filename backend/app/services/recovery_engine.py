from app.services.ai_copilot import ai_service
from app.services.validator import validator
from app.iot.gpio_controller import gpio_manager
from app.db.queries import log_recovery_attempt, save_robot_config, update_system_status
from app.models.schemas import ValidationResult, ControlLogic

class RecoveryEngine:
    
    def process_request(self, user_description: str):
        """
        Full pipeline: Describe -> Generate -> Validate
        Does NOT apply automatically unless specified, but primarily returns validation result.
        """
        # 1. Generate Logic
        logic = ai_service.generate_logic(user_description)
        
        # 2. Validate
        validation_result = validator.validate(logic)
        
        # 3. Log attempt
        log_status = "VALIDATED" if validation_result.is_safe else "REJECTED"
        log_recovery_attempt(log_status, f"Input: {user_description} | Result: {validation_result.message}")
        
        return validation_result

    def apply_recovery(self, logic: ControlLogic):
        """
        Applies the validated logic to hardware.
        """
        # Double check validation just in case
        validation = validator.validate(logic)
        if not validation.is_safe:
            return {"success": False, "message": f"Safety Violation: {validation.message}"}

        # Save Config to DB
        save_robot_config(logic)
        
        # Execute Hardware Action
        success = False
        if logic.action.upper() == "ON":
            success = gpio_manager.activate_pin(logic.pin)
        elif logic.action.upper() == "OFF":
            success = gpio_manager.deactivate_pin(logic.pin)
        else:
            # Default fallback for "motor_control" etc in this simple demo
            # We treat it as ON for demo
            success = gpio_manager.activate_pin(logic.pin)

        if success:
            update_system_status(f"ACTIVE: Pin {logic.pin} set to {logic.action}")
            log_recovery_attempt("APPLIED", f"Applied {logic.action} to Pin {logic.pin}")
            return {"success": True, "message": f"Successfully applied logic on Pin {logic.pin}"}
        else:
            update_system_status("ERROR")
            log_recovery_attempt("ERROR", f"Failed to apply logic on Pin {logic.pin}")
            return {"success": False, "message": "GPIO Hardware Failure"}

recovery_system = RecoveryEngine()
