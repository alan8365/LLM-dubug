import google.generativeai as genai
from openai import OpenAI


class CodeRepairAPIModule:
    def __init__(self, api_type, api_key, model_name=None):
        self.api_call = None

        self.api_type = api_type
        self.api_key = api_key
        self.prompt = self.default_prompt()
        self.model_name = model_name

        self.configure_api()

    def default_prompt(self):
        return f'''Fix the bugs in the following code:
```%s=
%s
```

Fixed code:
'''

    def configure_api(self):
        if self.api_type == "OpenAI":
            self.api_call = self.openai_api_config()
        elif self.api_type == "Gemini":
            self.api_call = self.google_api_config()
        else:
            raise ValueError("Unsupported API type")

    def openai_api_config(self):
        if self.model_name == 'gpt4':
            model_name = 'gpt-4'
        else:
            model_name = 'gpt-3.5-turbo'

        client = OpenAI()

        def api_call(prompt):
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.9,
                max_tokens=2048,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )

            return response.choices[0].message.content

        return api_call

    def google_api_config(self):
        genai.configure(api_key=self.api_key)
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
            convo = model.start_chat()
            convo.send_message(prompt)

            return convo.last.text

        return api_call

    def prepare_request(self, code_snippet, language):
        return {
            'code': code_snippet,
            'language': language
        }

    def make_api_call(self, payload):
        code_snippet = payload['code']
        language = payload['language']

        prompt = self.prompt % (language, code_snippet)
        return self.api_call(prompt)


if __name__ == "__main__":
    # Example usage of the module
    from dotenv import load_dotenv
    import os

    load_dotenv()

    # api_key = os.getenv("GOOGLE_API_KEY")
    api_key = os.getenv("OPENAI_API_KEY")

    api_module = CodeRepairAPIModule(api_type="OpenAI", api_key=api_key)
    payload = api_module.prepare_request("def greet(name): print('Hello, ' & name)", "Python")
    response = api_module.make_api_call(payload)
    print(response)
