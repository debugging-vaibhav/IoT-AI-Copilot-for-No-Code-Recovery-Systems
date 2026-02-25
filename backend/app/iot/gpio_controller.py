import logging
import platform

logger = logging.getLogger("uvicorn")

# Mock RPi.GPIO if not available (e.g., local dev on non-Pi)
try:
    import RPi.GPIO as GPIO
    IS_RPI = True
except (ImportError, RuntimeError):
    IS_RPI = False
    logger.warning("RPi.GPIO not found. Using Mock GPIO.")
    
    class MockGPIO:
        BCM = "BCM"
        OUT = "OUT"
        IN = "IN"
        HIGH = 1
        LOW = 0
        
        @staticmethod
        def setmode(mode):
            logger.info(f"MockGPIO: Set mode to {mode}")
            
        @staticmethod
        def setup(pin, mode):
            logger.info(f"MockGPIO: Setup pin {pin} as {mode}")
            
        @staticmethod
        def output(pin, state):
            logger.info(f"MockGPIO: Output {state} to pin {pin}")
            
        @staticmethod
        def cleanup():
            logger.info("MockGPIO: Cleanup")

    GPIO = MockGPIO()

class GPIOController:
    def __init__(self):
        self.mode_set = False
        
    def setup_board(self):
        """Initializes board mode."""
        if not self.mode_set:
            try:
                GPIO.setmode(GPIO.BCM)
                self.mode_set = True
                logger.info("GPIO Board Setup Complete (BCM Mode)")
            except Exception as e:
                logger.error(f"Failed to setup GPIO: {e}")

    def activate_pin(self, pin: int):
        """Sets a pin to HIGH."""
        self.setup_board()
        try:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.HIGH)
            logger.info(f"GPIO Pin {pin} ACTIVATED (HIGH)")
            return True
        except Exception as e:
            logger.error(f"Error activating pin {pin}: {e}")
            return False

    def deactivate_pin(self, pin: int):
        """Sets a pin to LOW."""
        self.setup_board()
        try:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)
            logger.info(f"GPIO Pin {pin} DEACTIVATED (LOW)")
            return True
        except Exception as e:
            logger.error(f"Error deactivating pin {pin}: {e}")
            return False

    def cleanup(self):
        GPIO.cleanup()
        self.mode_set = False

gpio_manager = GPIOController()
