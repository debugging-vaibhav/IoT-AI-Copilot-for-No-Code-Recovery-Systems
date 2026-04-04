"""
Sensor Controller — streams sensor values in background threads.
"""
import threading
import time
from logger import logger
from config import SIMULATE_HARDWARE

if SIMULATE_HARDWARE:
    class _MockGPIO:
        BCM = 11; IN = 1
        @staticmethod
        def setmode(m): pass
        @staticmethod
        def setwarnings(f): pass
        @staticmethod
        def setup(p, m): pass
        @staticmethod
        def input(p):
            import random
            return random.choice([0, 1])
    GPIO = _MockGPIO()
else:
    try:
        import RPi.GPIO as GPIO
    except ImportError:
        class _MockGPIO:
            BCM = 11; IN = 1
            @staticmethod
            def setmode(m): pass
            @staticmethod
            def setwarnings(f): pass
            @staticmethod
            def setup(p, m): pass
            @staticmethod
            def input(p): return 0
        GPIO = _MockGPIO()

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

sensor_threads = {}
sensor_values = {}  # latest readings: pin -> value
_stop_flags = {}


def sensor_loop(pin):
    GPIO.setup(pin, GPIO.IN)
    logger.info(f"Sensor streaming started on pin {pin}")

    while not _stop_flags.get(pin, False):
        try:
            value = GPIO.input(pin)
            sensor_values[pin] = value
            logger.debug(f"Sensor pin {pin} value: {value}")
            time.sleep(1)
        except Exception as e:
            logger.error(f"Sensor read error on pin {pin}: {e}")
            break

    logger.info(f"Sensor streaming stopped on pin {pin}")


def start_sensor_stream(pin):
    if pin in sensor_threads and sensor_threads[pin].is_alive():
        logger.warning(f"Sensor already streaming on pin {pin}")
        return False

    _stop_flags[pin] = False
    thread = threading.Thread(target=sensor_loop, args=(pin,), daemon=True)
    sensor_threads[pin] = thread
    thread.start()
    return True


def stop_sensor_stream(pin):
    _stop_flags[pin] = True
    if pin in sensor_threads:
        del sensor_threads[pin]
    logger.info(f"Sensor stream stop requested for pin {pin}")
    return True


def get_sensor_value(pin):
    return sensor_values.get(pin, None)
