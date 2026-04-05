"""
Sensor Controller — streams sensor values in background threads.
Uses gpiozero (works natively on Raspberry Pi 5).
"""
import threading
import time
from logger import logger
from config import SIMULATE_HARDWARE

sensor_threads = {}
sensor_values = {}  # latest readings: pin -> value
_stop_flags = {}


if SIMULATE_HARDWARE:
    def _read_pin(pin):
        import random
        return random.choice([0, 1])
else:
    from gpiozero import InputDevice
    _input_devices = {}

    def _read_pin(pin):
        if pin not in _input_devices:
            _input_devices[pin] = InputDevice(pin)
        return 1 if _input_devices[pin].is_active else 0


def sensor_loop(pin):
    logger.info(f"Sensor streaming started on pin {pin}")
    while not _stop_flags.get(pin, False):
        try:
            value = _read_pin(pin)
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
