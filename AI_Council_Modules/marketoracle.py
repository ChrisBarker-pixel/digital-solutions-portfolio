from .base_agent import BaseAgent

class MarketOracle(BaseAgent):
    def analyze_market(self, category: str, location: str) -> dict:
        prompt = f"Perform a gap analysis for '{category}' in '{location}'. Find top pricing tiers and SEO gaps."
        return self.send_message_to_groq([{"role": "user", "content": prompt}])