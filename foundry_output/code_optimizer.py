import google.generativeai as genai

class DPOptimizerAgent:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def optimize_code(self, user_code):
        prompt = f"""
        Identify the recurrence relation in this code: {user_code}.
        Rewrite it using a Bottom-Up Tabulation (DP) approach to eliminate redundant calculations.
        Provide the reasoning chain and the optimized code.
        """
        response = self.model.generate_content(prompt)
        return response.text