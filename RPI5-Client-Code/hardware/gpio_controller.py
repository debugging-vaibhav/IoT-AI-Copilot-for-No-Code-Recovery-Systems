"""
GPIO Controller — works with real RPi.GPIO or falls back to simulation.
"""
from logger import logger
from config import SIMULATE_HARDWARE

if SIMULATE_HARDWARE:
    logger.info("GPIO: Running in SIMULATION mode")

    class _MockGPIO:
        BCM = 11
        OUT = 0
        IN = 1

        @staticmethod
        def setmode(mode): pass

        @staticmethod
        def setwarnings(flag): pass

        @staticmethod
        def setup(pin, mode): pass

        @staticmethod
        def output(pin, value):
            logger.info(f"[SIM] GPIO output pin {pin} -> {value}")

        @staticmethod
        def input(pin):
            import random
            val = random.choice([0, 1])
            logger.info(f"[SIM] GPIO input pin {pin} -> {val}")
            return val

        @staticmethod
        def cleanup():
            logger.info("[SIM] GPIO cleanup")

    GPIO = _MockGPIO()
else:
    try:
        import RPi.GPIO as GPIO
        logger.info("GPIO: Using real RPi.GPIO")
    except ImportError:
        logger.warning("RPi.GPIO not available — falling back to simulation")
        # Re-use mock above
        class _MockGPIO:
            BCM = 11; OUT = 0; IN = 1
            @staticmethod
            def setmode(m): pass
            @staticmethod
            def setwarnings(f): pass
            @staticmethod
            def setup(p, m): pass
            @staticmethod
            def output(p, v): logger.info(f"[SIM] pin {p} -> {v}")
            @staticmethod
            def input(p): return 0
            @staticmethod
            def cleanup(): pass
        GPIO = _MockGPIO()

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


def write_pin(pin, value):
    """Set a digital output pin HIGH (1) or LOW (0)."""
    try:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, value)
        logger.info(f"Pin {pin} set to {value}")
        return True
    except Exception as e:
        logger.error(f"GPIO write failed on pin {pin}: {e}")
        return False


def read_pin(pin):
    """Read a digital input pin."""
    try:
        GPIO.setup(pin, GPIO.IN)
        value = GPIO.input(pin)
        logger.info(f"Pin {pin} read: {value}")
        return value
    except Exception as e:
        logger.error(f"GPIO read failed on pin {pin}: {e}")
        return None
