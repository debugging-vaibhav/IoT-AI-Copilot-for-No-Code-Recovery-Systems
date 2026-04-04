"""
LAM (Large Action Model) Engine — stub for local LLM inference.
In production, this loads a .gguf model and runs inference locally.
For the demo, it uses keyword-based parsing as a fallback.
"""
import json
import re
from logger import logger
from ai.prompt_templates import COMMAND_TEMPLATE


class LAMEngine:
    def __init__(self, model_path=None):
        self.model_path = model_path
        self.model = None
        self._try_load_model()

    def _try_load_model(self):
        """Attempt to load the local GGUF model."""
        if self.model_path:
            try:
                # In production: from llama_cpp import Llama
                # self.model = Llama(model_path=self.model_path)
                logger.info(f"LAM model would load from: {self.model_path}")
            except Exception as e:
                logger.warning(f"Could not load LAM model: {e}")
        else:
            logger.info("LAM Engine running in keyword-parsing mode (no model loaded)")

    def parse_instruction(self, instruction: str) -> dict:
        """
        Convert a natural language instruction to a command dict.
        Falls back to keyword parsing if no model is loaded.
        """
        if self.model:
            return self._infer_with_model(instruction)
        else:
            return self._keyword_parse(instruction)

    def _infer_with_model(self, instruction: str) -> dict:
        """Run inference with the loaded GGUF model."""
        # Placeholder for real model inference
        prompt = COMMAND_TEMPLATE.format(instruction=instruction)
        logger.info(f"Would run inference: {prompt[:80]}...")
        return self._keyword_parse(instruction)

    def _keyword_parse(self, instruction: str) -> dict:
        """Fallback: extract commands from keywords."""
        text = instruction.lower()

        # Try to extract pin number
        pin_match = re.search(r'pin\s*(\d+)', text)
        pin = int(pin_match.group(1)) if pin_match else 17  # default

        # Detect action
        if any(w in text for w in ["servo", "rotate", "angle", "degree"]):
            angle_match = re.search(r'(\d+)\s*(?:degrees?|°)', text)
            angle = int(angle_match.group(1)) if angle_match else 90
            return {"pin": pin, "action": "servo_control", "angle": angle}

        elif any(w in text for w in ["read", "sensor", "stream", "monitor"]):
            return {"pin": pin, "action": "sensor_stream"}

        elif any(w in text for w in ["off", "low", "stop", "disable"]):
            return {"pin": pin, "action": "off"}

        elif any(w in text for w in ["on", "high", "start", "enable", "turn"]):
            return {"pin": pin, "action": "on"}

        elif any(w in text for w in ["delete", "remove", "free", "release"]):
            return {"pin": pin, "action": "schema_delete"}

        else:
            return {"pin": pin, "action": "on"}


# Singleton instance
lam_engine = LAMEngine()
