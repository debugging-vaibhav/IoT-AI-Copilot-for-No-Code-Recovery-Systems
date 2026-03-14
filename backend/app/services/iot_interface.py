import logging
import requests
from app.core.config import settings

logger = logging.getLogger("uvicorn")

class IoTInterface:
    """
    Placeholder service layer for interacting with IoT hardware.
    In a real implementation, these methods would communicate with the IoT
    devices via APIs, message queues (like MQTT), or WebSockets.
    """
    
    def send_command(self, pin: int, action: str) -> bool:
        """
        Sends a command to the IoT hardware layer via HTTP POST.
        """
        logger.info(f"IoT Interface: Sending command '{action}' to pin {pin}")
        
        try:
            response = requests.post(f"{settings.IOT_SERVICE_URL}/execute", json={
                "pin": pin,
                "action": action.lower()
            }, timeout=5)
            response.raise_for_status()
            logger.info("IoT Interface: Command sent successfully.")
            return True
        except requests.exceptions.RequestException as e:
            logger.error(f"IoT Interface Error: Could not reach hardware service at {settings.IOT_SERVICE_URL}. {e}")
            return False

    def get_device_status(self) -> dict:
        """
        Retrieves the current status of the connected IoT devices via HTTP GET.
        """
        logger.info("IoT Interface: Fetching device status")
        try:
            response = requests.get(f"{settings.IOT_SERVICE_URL}/status", timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.warning(f"IoT Interface Error: Could not fetch status from hardware service. {e}")
            return {"status": "ERROR", "hardware": "OFFLINE", "details": str(e)}

iot_interface = IoTInterface()
