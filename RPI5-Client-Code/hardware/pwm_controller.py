"""
PWM Controller for servos — uses gpiozero (works natively on Raspberry Pi 5).
"""
import time
from logger import logger
from config import SIMULATE_HARDWARE

if SIMULATE_HARDWARE:
    logger.info("PWM: Running in SIMULATION mode")

    def move_servo(pin, angle):
        logger.info(f"[SIM] Servo on pin {pin} moved to {angle} degrees")
        return True

else:
    from gpiozero import Servo

    logger.info("PWM: Using gpiozero Servo")
    _servos = {}

    def move_servo(pin, angle):
        """Move servo on `pin` to `angle` (0-180 degrees)."""
        try:
            if pin not in _servos:
                _servos[pin] = Servo(pin)

            servo = _servos[pin]
            # gpiozero Servo uses -1 (0°) to +1 (180°), convert from 0-180
            value = (angle / 90.0) - 1.0
            servo.value = max(-1.0, min(1.0, value))
            time.sleep(0.5)
            servo.value = None  # detach to stop jitter

            logger.info(f"Servo on pin {pin} moved to {angle} degrees")
            return True
        except Exception as e:
            logger.error(f"Servo control failed on pin {pin}: {e}")
            return False
