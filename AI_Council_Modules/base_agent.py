import json
import requests

class BaseAgent:
    def __init__(self, agent_name="BaseAgent"):
        self.agent_name = agent_name
        # Note: In the Zenith GUI, the API key is handled by the main engine
        # This base class is designed to be lean and modular
        
    def send_message_to_groq(self, messages):
        """Standardized Groq Latch for all agents."""
        # This is a placeholder for your specific Groq/API call logic
        # For now, it relays back to the engine's log for transparency
        return {"status": "SUCCESS", "agent": self.agent_name, "message": "Logic Latched."}

    def log_to_engine(self, msg, status="INFO"):
        print(f"[{self.agent_name}] {status}: {msg}")