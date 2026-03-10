import os
from dotenv import load_dotenv

load_dotenv()

NGROK_URL = os.getenv("NGROK_URL")
MODEL_PATH = os.getenv("MODEL_PATH")

POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", 5))
RAG_TOP_K = int(os.getenv("RAG_TOP_K", 3))

DEBUG_MODE = os.getenv("DEBUG_MODE", "False") == "True"

# Hardware safety limits
MAX_SERVO_ANGLE = 180
MIN_SERVO_ANGLE = 0

# Allowed pins (BCM)
AVAILABLE_PINS = [
    4, 17, 18, 22, 23, 24, 25, 27  # Still need to verify which pins are actually available on the RPI5 and not used by other peripherals
]