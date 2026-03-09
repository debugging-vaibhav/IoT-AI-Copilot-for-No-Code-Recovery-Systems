import threading
import time

import RPi.GPIO as GPIO

from logger import logger

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

sensor_threads = {}


def sensor_loop(pin):

    GPIO.setup(pin, GPIO.IN)

    logger.info(f"Sensor streaming started on pin {pin}")

    while True:

        try:

            value = GPIO.input(pin)

            logger.info(f"Sensor {pin} value: {value}")

            time.sleep(1)

        except Exception as e:

            logger.error(f"Sensor read error: {e}")

            break


def start_sensor_stream(pin):

    if pin in sensor_threads:

        logger.warning("Sensor already streaming")

        return

    thread = threading.Thread(
        target=sensor_loop,
        args=(pin,),
        daemon=True
    )

    sensor_threads[pin] = thread

    thread.start()