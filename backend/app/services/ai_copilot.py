"""
AI Copilot service — calls the AI-LAM-Server for LLM-powered intent parsing.
Falls back to keyword-based parsing if the LAM server is unreachable.
"""
import logging
import os
import httpx

from app.models.schemas import ControlLogic

logger = logging.getLogger("uvicorn")

LAM_SERVER_URL = os.getenv("LAM_SERVER_URL", "http://localhost:8100")


class AICopilot:

    def generate_logic(self, description: str) -> ControlLogic:
        """
        Convert natural-language description into ControlLogic.
        Tries the AI-LAM-Server first, falls back to keyword parsing.
        """
        try:
            return self._call_lam_server(description)
        except Exception as exc:
            logger.warning("AI-LAM-Server unavailable (%s), using keyword fallback", exc)
            return self._keyword_fallback(description)

    def _call_lam_server(self, description: str) -> ControlLogic:
        """Call the AI-LAM-Server /process endpoint."""
        resp = httpx.post(
            f"{LAM_SERVER_URL}/process",
            json={"description": description},
            timeout=30.0,
        )
        resp.raise_for_status()
        data = resp.json()

        commands = data.get("commands", [])
        reasoning = data.get("reasoning", "")

        if not commands:
            raise ValueError("LAM server returned no commands")

        cmd = commands[0]  # use the first command for ControlLogic
        action = cmd.get("action", "on").upper()
        pin = cmd.get("pin", 17)
        angle = cmd.get("angle")

        sensor = self._detect_sensor(description)
        rule = reasoning or f"AI-generated: {action} on PIN {pin}"

        return ControlLogic(
            sensor=sensor,
            pin=pin,
            action=action,
            rule=rule,
            angle=angle,
        )

    def _keyword_fallback(self, description: str) -> ControlLogic:
        """Original keyword-based parser as fallback."""
        description_lower = description.lower()
        pin = 17

        words = description_lower.split()
        for i, word in enumerate(words):
            if word == "pin" and i + 1 < len(words):
                try:
                    pin = int(words[i + 1])
                except ValueError:
                    pass

        action = "ON" if "on" in description_lower else "OFF"
        sensor = self._detect_sensor(description)
        rule = f"IF {sensor}_value > threshold THEN set PIN_{pin} {action}"

        return ControlLogic(sensor=sensor, pin=pin, action=action, rule=rule)

    @staticmethod
    def _detect_sensor(description: str) -> str:
        description_lower = description.lower()
        if "ultrasonic" in description_lower:
            return "ultrasonic"
        if "temp" in description_lower:
            return "temperature"
        if "lidar" in description_lower:
            return "lidar"
        if "gps" in description_lower:
            return "gps"
        if "servo" in description_lower or "motor" in description_lower:
            return "servo"
        return "generic_sensor"


ai_service = AICopilot()
