"""
LangChain tool definitions for the hardware actions.
These tools do NOT execute hardware — they return structured command dicts
that the backend will forward to the RPi5.
"""
from langchain_core.tools import tool


@tool
def servo_control(pin: int, angle: float) -> dict:
    """Move a servo motor to a specific angle. Pin must be a safe GPIO BCM pin. Angle range: 0-180 degrees."""
    return {"pin": pin, "action": "servo_control", "angle": angle}


@tool
def pin_write_on(pin: int) -> dict:
    """Set a GPIO pin to HIGH (turn on). Pin must be a safe GPIO BCM pin."""
    return {"pin": pin, "action": "on"}


@tool
def pin_write_off(pin: int) -> dict:
    """Set a GPIO pin to LOW (turn off). Pin must be a safe GPIO BCM pin."""
    return {"pin": pin, "action": "off"}


@tool
def sensor_stream(pin: int) -> dict:
    """Start continuous sensor reading on a GPIO pin. Pin must be a safe GPIO BCM pin."""
    return {"pin": pin, "action": "sensor_stream"}


@tool
def schema_delete(pin: int) -> dict:
    """Stop control on a GPIO pin and free the resource. Pin must be a safe GPIO BCM pin."""
    return {"pin": pin, "action": "schema_delete"}


ALL_TOOLS = [servo_control, pin_write_on, pin_write_off, sensor_stream, schema_delete]
