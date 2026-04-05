"""
GPIO Controller — uses gpiozero (works natively on Raspberry Pi 5).
"""
from logger import logger
from config import SIMULATE_HARDWARE

if SIMULATE_HARDWARE:
    logger.info("GPIO: Running in SIMULATION mode")
    _sim_pins = {}

    def write_pin(pin, value):
        _sim_pins[pin] = value
        logger.info(f"[SIM] Pin {pin} set to {value}")
        return True

    def read_pin(pin):
        import random
        val = random.choice([0, 1])
        logger.info(f"[SIM] Pin {pin} read: {val}")
        return val

else:
    from gpiozero import LED, Button

    logger.info("GPIO: Using gpiozero")
    _output_devices = {}

    def write_pin(pin, value):
        try:
            if pin not in _output_devices:
                _output_devices[pin] = LED(pin)
            dev = _output_devices[pin]
            if value:
                dev.on()
            else:
                dev.off()
            logger.info(f"Pin {pin} set to {value}")
            return True
        except Exception as e:
            logger.error(f"GPIO write failed on pin {pin}: {e}")
            return False

    def read_pin(pin):
        try:
            btn = Button(pin)
            value = 1 if btn.is_pressed else 0
            btn.close()
            logger.info(f"Pin {pin} read: {value}")
            return value
        except Exception as e:
            logger.error(f"GPIO read failed on pin {pin}: {e}")
            return None
