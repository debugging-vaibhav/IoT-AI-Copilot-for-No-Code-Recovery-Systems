from app.services.ai_copilot import ai_service
from app.services.validator import validator
from app.services.iot_interface import iot_interface
from app.db.queries import log_recovery_attempt, save_robot_config, update_system_status, DatabaseConnectionError
from app.models.schemas import ValidationResult, ControlLogic
import logging

logger = logging.getLogger("uvicorn")

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
        try:
            log_recovery_attempt(log_status, f"Input: {user_description} | Result: {validation_result.message}")
        except DatabaseConnectionError as e:
            logger.error(f"Failed to log recovery attempt: {e}")
            # Continuing execution since the core validate task still succeeded.
        
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
        try:
            save_robot_config(logic)
        except DatabaseConnectionError as e:
            logger.error(f"Database error saving config: {e}")
            return {"success": False, "message": f"Database unavailable: {e}"}
        
        # Execute Hardware Action (via HTTP abstract interface)
        success = iot_interface.send_command(pin=logic.pin, action=logic.action)

        if success:
            try:
                update_system_status(f"ACTIVE: Pin {logic.pin} set to {logic.action}")
                log_recovery_attempt("APPLIED", f"Applied {logic.action} to Pin {logic.pin}")
            except DatabaseConnectionError:
                 pass # We ignore logging errors if the hardware action succeeded
            return {"success": True, "message": f"Successfully applied logic on Pin {logic.pin}"}
        else:
            try:
                update_system_status("ERROR")
                log_recovery_attempt("ERROR", f"Failed to apply logic on Pin {logic.pin}")
            except DatabaseConnectionError:
                 pass
            return {"success": False, "message": "IoT Communication Failure. IoT service is unreachable."}

recovery_system = RecoveryEngine()
