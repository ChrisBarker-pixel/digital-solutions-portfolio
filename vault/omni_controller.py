import os, json, re
from groq import Groq


class OmniController:
    def __init__(self, app_instance):
        self.app = app_instance
        self.api_key = os.environ.get("GROQ_API_KEY")
        self.client = Groq(api_key=self.api_key)
        self.model = "llama-3.3-70b-versatile"
        self.system_prompt = "Output RAW JSON. Format: {'lattice_data': {'1': {'title': '', 'logic': '', 'color': ''}}}"

    def generate_node_logic(self, prompt_text):
        """🧠 THE LOGIC GENERATOR: V4.1 (Strip-to-Brace)"""
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "system", "content": self.system_prompt}, {"role": "user", "content": prompt_text}]
            )
            raw_text = completion.choices[0].message.content

            # 1. THE BRACE LATCH: Find the absolute start and end of the JSON object
            # This kills the "Char 1" and "Expecting property name" errors caused by Markdown
            start_idx = raw_text.find('{')
            end_idx = raw_text.rfind('}') + 1

            if start_idx != -1 and end_idx != 0:
                clean_json = raw_text[start_idx:end_idx].strip()

                # 2. INTERNAL CODE CLEANING: Escape newlines only inside "quotes"
                def escape_logic(m):
                    return m.group(0).replace('\n', '\\n').replace('\t', '\\t')

                clean_json = re.sub(r'(".*?")', escape_logic, clean_json, flags=re.DOTALL)

                # 3. THE "SINGLE-QUOTE" REPAIR: If the AI used ' instead of " for keys
                clean_json = re.sub(r"'(?=\s*\w+\s*':)", '"', clean_json)  # Fix key start
                clean_json = re.sub(r"(?<=\w)':", '":', clean_json)  # Fix key end

                # 4. FINAL PARSE
                return json.loads(clean_json)

            self.app.log_system("❌ OMNI_ERR: No braces found in AI response.")
            return None
        except Exception as e:
            self.app.log_system(f"❌ NEURAL_GEN_ERR: {str(e)[:50]}")
            return None