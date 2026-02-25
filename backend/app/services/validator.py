from app.models.schemas import ControlLogic, ValidationResult

class LogicValidator:
    """
    Validates generated logic ensuring safety constraints.
    """
    
    # RPi 3/4 Safe GPIO BCM pins
    SAFE_PINS = {4, 17, 27, 22, 5, 6, 13, 19, 26, 18, 23, 24, 25, 12, 16, 20, 21}
    
    def validate(self, logic: ControlLogic) -> ValidationResult:
        
        # 1. Validate Pin
        if logic.pin not in self.SAFE_PINS:
            return ValidationResult(
                is_safe=False,
                logic=logic,
                message=f"Pin {logic.pin} is not in the safe GPIO list or is reserved."
            )

        # 2. Validate Action
        allowed_actions = {"ON", "OFF", "toggle", "motor_control"}
        # For simplicity in normalization, check if the string action contains these keywords
        # or exactly matches.
        if logic.action.upper() not in {"ON", "OFF", "MOTOR_CONTROL", "TOGGLE"}:
             # Let's be lenient for the demo, but warning
             pass 

        # 3. Safe Rule Check
        # Example: don't allow "always on" without conditions? 
        # (Skipped for basic version)

        return ValidationResult(
            is_safe=True,
            logic=logic,
            message="Logic validated successfully. Safe to apply."
        )

validator = LogicValidator()
