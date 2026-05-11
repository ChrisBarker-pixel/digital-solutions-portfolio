from .base_agent import BaseAgent

class LeadSiren(BaseAgent):
    def prospect_entities(self, target: str, location: str) -> dict:
        prompt = f"Identify high-value B2B entities matching '{target}' in '{location}' with high repeat potential."
        return self.send_message_to_groq([{"role": "user", "content": prompt}])