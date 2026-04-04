"""
IoT Interface — communicates with the RPi hardware layer via HTTP.
Now uses the device registry to find the RPi dynamically.
"""
import logging
import requests
from app.core.config import settings
from app.services.device_registry import get_primary_device_url

logger = logging.getLogger("uvicorn")


class IoTInterface:

    def _get_device_url(self) -> str:
        """Get the URL of the connected RPi device."""
        # First try the device registry (dynamic)
        url = get_primary_device_url()
        if url:
            return url
        # Fall back to config
        logger.warning("No registered device found, using fallback IOT_SERVICE_URL")
        return settings.IOT_SERVICE_URL

    def send_command(self, pin: int, action: str, angle: float | None = None) -> bool:
        """Send a command to the RPi hardware layer via HTTP POST."""
        device_url = self._get_device_url()
        logger.info(f"IoT Interface: Sending '{action}' to pin {pin} via {device_url}")

        payload = {"pin": pin, "action": action.lower()}
        if angle is not None:
            payload["angle"] = angle

        try:
            response = requests.post(f"{device_url}/execute", json=payload, timeout=5)
            response.raise_for_status()
            data = response.json()
            logger.info(f"IoT Interface: Response — {data}")
            return data.get("success", True)
        except requests.exceptions.RequestException as e:
            logger.error(f"IoT Interface Error: Could not reach {device_url}. {e}")
            return False

    def get_device_status(self) -> dict:
        """Fetch live status from the RPi."""
        device_url = self._get_device_url()
        logger.info(f"IoT Interface: Fetching status from {device_url}")

        try:
            response = requests.get(f"{device_url}/status", timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.warning(f"IoT Interface: Could not fetch status. {e}")
            return {
                "status": "UNREACHABLE",
                "hardware": "OFFLINE",
                "error": str(e),
            }


iot_interface = IoTInterface()
