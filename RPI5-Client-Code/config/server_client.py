import requests

from config import NGROK_URL
from logger import logger


def fetch_goal():

    try:

        response = requests.get(NGROK_URL, timeout=5)

        if response.status_code == 200:

            data = response.json()

            goal = data.get("goal") or data.get("instruction")

            return goal

    except Exception as e:

        logger.error(f"Server fetch failed: {e}")

    return None