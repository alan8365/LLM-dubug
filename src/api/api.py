import google.generativeai as genai

class CodeRepairAPIModule:
    def __init__(self, api_type, api_key, language):
        self.api_call = None

        self.api_type = api_type
        self.api_key = api_key
        self.language = language
        self.prompt = self.default_prompt()
        self.configure_api()

    def default_prompt(self):
        return f'''Fix the bugs in the following code:
```{self.language}=
%s
```

Fixed code:
'''

    def update_prompt(self, new_prompt):
        self.prompt = new_prompt

    def configure_api(self):
        if self.api_type == "OpenAI":
            self.endpoint = "https://api.openai.com/v1/engines/..."
        elif self.api_type == "Gemini":
            self.api_call = self.google_api_config()
        else:
            raise ValueError("Unsupported API type")

    def google_api_config(self):
        generation_config = {
            "temperature": 0.9,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,
        }
        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_ONLY_HIGH"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_ONLY_HIGH"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_ONLY_HIGH"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_ONLY_HIGH"
            },
        ]

        model = genai.GenerativeModel(model_name="gemini-pro",
                                      generation_config=generation_config,
                                      safety_settings=safety_settings)

        def api_call(prompt):
            prompt_parts = [
                prompt,
            ]
            response = model.generate_content(prompt_parts)

            return response.text

    def prepare_request(self, code_snippet):
        if self.api_type == "OpenAI":
            payload = {"prompt": self.prompt + "\n" + code_snippet, "max_tokens": 150}
        elif self.api_type == "Gemini":
            payload = {"input": code_snippet, "context": self.prompt}
        else:
            raise ValueError("Unsupported API type")
        return payload

    def make_api_call(self, payload):
        pass

    def process_response(self, response):
        if not response:
            return "No response received or an error occurred."

        if self.api_type == "OpenAI":
            return response.get("choices", [{}])[0].get("text", "").strip()
        elif self.api_type == "Gemini":
            return response.get("output", "").strip()


if __name__ == "__main__":
    # Example usage of the module
    api_module = CodeRepairAPIModule(api_type="OpenAI", api_key="your-openai-api-key")
    payload = api_module.prepare_request("def greet(name): print('Hello, ' + name)")
    response = api_module.make_api_call(payload)
    repaired_code = api_module.process_response(response)
    print(repaired_code)
