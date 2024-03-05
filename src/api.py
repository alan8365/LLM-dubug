from openai import OpenAI
from dotenv import load_dotenv

from google import generativeai as genai  # type: ignore

from prompt import Prompt
from quixbugs import QuixBugsDataset, QuixBugsSample
from patch import Patch, PatchGroup
from src_types import MODEL_NAME

import os
import time
from typing import Optional
from abc import ABC, abstractmethod

load_dotenv()


class LlmApi(ABC):
    @abstractmethod
    def __init__(self, model_name: MODEL_NAME) -> None:
        self.model_name = model_name
        self.api_key: Optional[str] = ""

        raise NotImplementedError

    @abstractmethod
    def get_repaired_code(self, prompt: Prompt):
        raise NotImplementedError

    def api_call(self, prompt: Prompt) -> tuple[Optional[str], float]:
        start = time.time()
        repaired_code = self.get_repaired_code(prompt)
        end = time.time()

        run_time = end - start

        return repaired_code, run_time

    def get_patch(self, prompt: Prompt, patch_id: int) -> Patch:
        repaired_code, run_time = self.api_call(prompt)
        patch = Patch(patch_id, repaired_code, run_time)

        return patch

    def patch_group_generator(self, prompt: Prompt) -> PatchGroup:
        patchs = [self.get_patch(prompt, i) for i in range(3)]
        patch_group = PatchGroup(patchs, prompt, self.model_name)

        return patch_group


class OpenAiApi(LlmApi):
    def __init__(self, model_name: MODEL_NAME) -> None:
        super().__init__(model_name)
        model_name_list = ["gpt-3.5-turbo-0125", "gpt-4"]
        if not model_name in model_name_list:
            raise ValueError(
                f"Invalid model name provided: {model_name}. Please choose from {model_name_list}"
            )

        self.model_name = model_name
        self.api_key = os.getenv("OPENAI_API_KEY")

    def get_repaired_code(self, prompt: Prompt) -> Optional[str]:
        client = OpenAI()
        response = client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt.prompt}],
            temperature=0.9,
            max_tokens=2048,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )

        repaired_code = response.choices[0].message.content

        return repaired_code


class GeminiApi(LlmApi):
    def __init__(self, model_name: MODEL_NAME) -> None:
        model_name_list = ["gemini-1.0-pro"]
        if not model_name in model_name_list:
            raise ValueError(
                f"Invalid model name provided: {model_name}. Please choose from {model_name_list}"
            )

        self.model_name = model_name
        self.api_key = os.getenv("GOOGLE_API_KEY")
        genai.configure(api_key=self.api_key, transport='rest')

    def get_config(self):
        generation_config = {
            "temperature": 0.9,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,
        }
        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_ONLY_HIGH"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_ONLY_HIGH"},
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_ONLY_HIGH",
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_ONLY_HIGH",
            },
        ]

        return generation_config, safety_settings

    def get_repaired_code(self, prompt: Prompt):
        generation_config, safety_settings = self.get_config()

        model = genai.GenerativeModel(
            model_name=self.model_name,
            generation_config=generation_config,
            safety_settings=safety_settings,
        )

        convo = model.start_chat()
        convo.send_message(prompt.prompt)

        return convo.last.text


if __name__ == "__main__":
    dataset = QuixBugsDataset("python")
    prompt = Prompt(dataset[0])

    # model_name: MODEL_NAME = "gpt-3.5-turbo-0125"
    model_name: MODEL_NAME = "gemini-1.0-pro"
    a = GeminiApi(model_name)

    patch = a.get_patch(prompt, 0)

    print(patch)

    # GOOGLE_API_KEY="AIzaSyDGuEKKmbihmn3Di5kfVyoqBAYke4dGycs"
    # genai.configure(api_key=GOOGLE_API_KEY)
    # model = genai.GenerativeModel('gemini-pro')
    # response = model.generate_content("What is the meaning of life?", request_options={'timeout': 1000})

    # print(response.text)
