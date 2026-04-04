"""
PWM Controller for servos/motors — simulation-aware.
"""
import time
from logger import logger
from config import SIMULATE_HARDWARE

if SIMULATE_HARDWARE:
    class _MockGPIO:
        BCM = 11; OUT = 0
        @staticmethod
        def setmode(m): pass
        @staticmethod
        def setwarnings(f): pass
        @staticmethod
        def setup(p, m): pass

        class PWM:
            def __init__(self, pin, freq):
                self.pin = pin
                self.freq = freq
            def start(self, dc):
                logger.info(f"[SIM] PWM start pin {self.pin} freq={self.freq} dc={dc}")
            def ChangeDutyCycle(self, dc):
                logger.info(f"[SIM] PWM pin {self.pin} duty={dc:.2f}")
            def stop(self):
                logger.info(f"[SIM] PWM stop pin {self.pin}")
        @staticmethod
        def cleanup(): pass

    GPIO = _MockGPIO()
else:
    try:
        import RPi.GPIO as GPIO
    except ImportError:
        class _MockGPIO:
            BCM = 11; OUT = 0
            @staticmethod
            def setmode(m): pass
            @staticmethod
            def setwarnings(f): pass
            @staticmethod
            def setup(p, m): pass
            class PWM:
                def __init__(self, pin, freq): self.pin = pin
                def start(self, dc): pass
                def ChangeDutyCycle(self, dc): logger.info(f"[SIM] PWM duty={dc:.2f}")
                def stop(self): pass
            @staticmethod
            def cleanup(): pass
        GPIO = _MockGPIO()

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

pwm_instances = {}


def move_servo(pin, angle):
    """Move servo on `pin` to `angle` (0-180 degrees)."""
    try:
        GPIO.setup(pin, GPIO.OUT)

        if pin not in pwm_instances:
            pwm = GPIO.PWM(pin, 50)
            pwm.start(0)
            pwm_instances[pin] = pwm

        pwm = pwm_instances[pin]
        duty = 2 + (angle / 18)
        pwm.ChangeDutyCycle(duty)
        time.sleep(0.5)
        pwm.ChangeDutyCycle(0)  # stop jitter

        logger.info(f"Servo on pin {pin} moved to {angle}°")
        return True
    except Exception as e:
        logger.error(f"Servo control failed on pin {pin}: {e}")
        return False
