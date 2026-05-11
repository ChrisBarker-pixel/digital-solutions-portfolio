from .base_agent import BaseAgent

class WebAppDesigner(BaseAgent):
    def create_user_interface(self, prompt: str, other_agent_outputs=None) -> dict:
        user_content = f"As a Web App Designer, {prompt}. Synthesis context: {other_agent_outputs}. Respond in JSON with: 'synthesized_ui_design', 'influenced_by', 'final_ui_recommendations'."
        return self.send_message_to_groq([{"role": "user", "content": user_content}])
