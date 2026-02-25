from app.models.schemas import ControlLogic
import random

class AICopilot:
    """
    Simulates an AI Copilot that parses natural language into structured control logic.
    In a real implementation, this would call OpenAI/Gemini APIs.
    """
    
    def generate_logic(self, description: str) -> ControlLogic:
        # Simple heuristic or random generation for demo purposes
        description_lower = description.lower()
        
        pin = 17 # Default safe pin
        
        # Try to extract pin from text
        words = description_lower.split()
        for i, word in enumerate(words):
            if word == "pin" and i + 1 < len(words):
                try:
                    pin = int(words[i+1])
                except ValueError:
                    pass

        action = "ON" if "on" in description_lower else "OFF"
        sensor = "generic_sensor"
        if "ultrasonic" in description_lower:
            sensor = "ultrasonic"
        elif "temp" in description_lower:
            sensor = "temperature"
            
        rule = f"IF {sensor}_value > threshold THEN set PIN_{pin} {action}"

        return ControlLogic(
            sensor=sensor,
            pin=pin,
            action=action,
            rule=rule
        )

ai_service = AICopilot()
