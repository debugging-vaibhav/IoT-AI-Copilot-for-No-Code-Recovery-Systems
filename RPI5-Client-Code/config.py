import os
from dotenv import load_dotenv

load_dotenv()

SERVER_URL = os.getenv("SERVER_URL", "http://localhost:8000")
DEVICE_ID = os.getenv("DEVICE_ID", "rpi-5-001")
RPI_PORT = int(os.getenv("RPI_PORT", "5000"))
SIMULATE_HARDWARE = os.getenv("SIMULATE_HARDWARE", "False").lower() in ("true", "1", "yes")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
