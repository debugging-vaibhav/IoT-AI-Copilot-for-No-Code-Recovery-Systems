"""
Execution Engine — receives validated commands and dispatches to hardware.
"""
from logger import logger
from control.schema_validator import validate_command, save_active_schema, delete_schema
from control.pin_manager import set_pin_state, release_pin
from hardware.gpio_controller import write_pin
from hardware.pwm_controller import move_servo
from hardware.sensor_controller import start_sensor_stream, stop_sensor_stream


def execute_command(command: dict) -> dict:
    """
    Execute a hardware command after validation.
    Returns {"success": bool, "message": str}
    """
    # Step 1: Validate
    validation = validate_command(command)
    if not validation["valid"]:
        logger.warning(f"Command rejected: {validation['reason']}")
        return {"success": False, "message": validation["reason"]}

    action = command["action"].lower()
    pin = int(command["pin"])

    try:
        # Step 2: Execute based on action type
        if action == "on":
            write_pin(pin, 1)
            set_pin_state(pin, "ON")
            save_active_schema(pin, {"action": "on", "pin": pin})
            return {"success": True, "message": f"Pin {pin} set to ON"}

        elif action == "off":
            write_pin(pin, 0)
            set_pin_state(pin, "OFF")
            save_active_schema(pin, {"action": "off", "pin": pin})
            return {"success": True, "message": f"Pin {pin} set to OFF"}

        elif action == "servo_control":
            angle = float(command.get("angle", 90))
            move_servo(pin, angle)
            set_pin_state(pin, "SERVO", {"angle": angle})
            save_active_schema(pin, {"action": "servo_control", "pin": pin, "angle": angle})
            return {"success": True, "message": f"Servo on pin {pin} moved to {angle}°"}

        elif action == "sensor_stream":
            start_sensor_stream(pin)
            set_pin_state(pin, "STREAMING")
            save_active_schema(pin, {"action": "sensor_stream", "pin": pin})
            return {"success": True, "message": f"Sensor stream started on pin {pin}"}

        elif action == "schema_delete":
            stop_sensor_stream(pin)
            release_pin(pin)
            delete_schema(pin)
            return {"success": True, "message": f"Pin {pin} released and schema deleted"}

        else:
            return {"success": False, "message": f"Unhandled action: {action}"}

    except Exception as e:
        logger.error(f"Execution failed: {e}")
        return {"success": False, "message": f"Execution error: {str(e)}"}
