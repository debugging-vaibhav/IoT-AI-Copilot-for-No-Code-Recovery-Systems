import RPi.GPIO as GPIO
import time

from logger import logger

pwm_instances = {}

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


def move_servo(pin, angle):

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

        logger.info(f"Servo moved on pin {pin} to {angle}")

    except Exception as e:

        logger.error(f"Servo control failed: {e}")