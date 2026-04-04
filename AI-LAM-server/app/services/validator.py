"""
Constraint validator — checks that LLM-produced commands are safe
before they are returned to the backend.
"""
from __future__ import annotations

from app.config import SAFE_PINS, ALLOWED_ACTIONS, SERVO_ANGLE_MIN, SERVO_ANGLE_MAX


def validate_command(cmd: dict) -> tuple[bool, str]:
    """
    Validate a single hardware command dict.
    Returns (is_valid, reason).
    """
    action = cmd.get("action", "").lower()
    pin = cmd.get("pin")

    # Action check
    if action not in ALLOWED_ACTIONS:
        return False, f"Unknown action '{action}'. Allowed: {', '.join(sorted(ALLOWED_ACTIONS))}"

    # Pin check
    if pin is None:
        return False, "Missing 'pin' field"
    try:
        pin = int(pin)
    except (TypeError, ValueError):
        return False, f"Pin must be an integer, got '{pin}'"
    if pin not in SAFE_PINS:
        return False, f"Pin {pin} is not in the safe GPIO set: {sorted(SAFE_PINS)}"

    # Servo-specific
    if action == "servo_control":
        angle = cmd.get("angle")
        if angle is None:
            return False, "servo_control requires an 'angle' parameter"
        try:
            angle = float(angle)
        except (TypeError, ValueError):
            return False, f"Angle must be a number, got '{angle}'"
        if not (SERVO_ANGLE_MIN <= angle <= SERVO_ANGLE_MAX):
            return False, f"Angle {angle} out of range [{SERVO_ANGLE_MIN}, {SERVO_ANGLE_MAX}]"

    return True, "ok"


def validate_commands(commands: list[dict]) -> tuple[bool, str]:
    """Validate a list of commands. Stops on first failure."""
    if not commands:
        return False, "No commands generated"

    for i, cmd in enumerate(commands):
        valid, reason = validate_command(cmd)
        if not valid:
            return False, f"Command #{i + 1} invalid: {reason}"

    return True, "All commands validated successfully"
