from app.models.schemas import ControlLogic, ValidationResult


class LogicValidator:
    """Validates generated logic ensuring safety constraints."""

    # RPi 3/4/5 Safe GPIO BCM pins
    SAFE_PINS = {4, 5, 6, 12, 13, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27}

    def validate(self, logic: ControlLogic) -> ValidationResult:
        # 1. Validate Pin
        if logic.pin not in self.SAFE_PINS:
            return ValidationResult(
                is_safe=False,
                logic=logic,
                message=f"Pin {logic.pin} is not in the safe GPIO list or is reserved."
            )

        # 2. Validate Action
        allowed = {"ON", "OFF", "MOTOR_CONTROL", "TOGGLE", "SERVO_CONTROL", "SENSOR_STREAM", "SCHEMA_DELETE"}
        if logic.action.upper() not in allowed:
            return ValidationResult(
                is_safe=False,
                logic=logic,
                message=f"Action '{logic.action}' is not recognized. Allowed: {allowed}"
            )

        return ValidationResult(
            is_safe=True,
            logic=logic,
            message="Logic validated successfully. Safe to apply."
        )


validator = LogicValidator()
