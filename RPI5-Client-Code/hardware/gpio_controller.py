import RPi.GPIO as GPIO

from logger import logger

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


def write_pin(pin, value):

    try:

        GPIO.setup(pin, GPIO.OUT)

        GPIO.output(pin, value)

        logger.info(f"Pin {pin} set to {value}")

    except Exception as e:

        logger.error(f"GPIO write failed: {e}")