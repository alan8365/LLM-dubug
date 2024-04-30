from openai import OpenAI
from dotenv import load_dotenv

from google import generativeai as genai  # type: ignore
from anthropic import Anthropic


from prompt import Prompt
from quixbugs import QuixBugsDataset, QuixBugsSample
from patch import Patch, PatchGroup
from src_types import MODEL_NAME

import os
import re
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
    def get_repaired_response(self, prompt: Prompt):
        raise NotImplementedError

    def api_call(self, prompt: Prompt) -> tuple[str, float]:
        start = time.time()
        repaired_response = self.get_repaired_response(prompt)
        end = time.time()

        run_time = end - start

        return repaired_response, run_time

    # TODO move to eval
    def clean_response(self, prompt: Prompt, response) -> str:
        lang = prompt.sample.language
        pattern = re.compile(rf"```{lang}=?(.*?)```", re.MULTILINE | re.DOTALL)
        find_all = pattern.findall(response)

        if find_all:
            cleaned_code = find_all[0]
        else:
            raise ValueError(f"Pattern error:\n {response}")

        return cleaned_code

    def get_patch(self, prompt: Prompt, patch_id: int) -> Patch:
        repaired_response, run_time = self.api_call(prompt)
        repaired_code = self.clean_response(prompt, repaired_response)
        patch = Patch(patch_id, repaired_response, repaired_code, run_time)

        return patch

    def get_patch_group(self, prompt: Prompt) -> PatchGroup:
        patchs = [self.get_patch(prompt, i) for i in range(3)]
        patch_group = PatchGroup(patchs, prompt, self.model_name)

        return patch_group

    @abstractmethod
    def __str__(self):
        raise NotImplementedError


class OpenAiApi(LlmApi):
    def __init__(self, model_name: MODEL_NAME) -> None:
        model_name_list = ["gpt-3.5-turbo-0125", "gpt-4-turbo-2024-04-09"]
        if not model_name in model_name_list:
            raise ValueError(
                f"Invalid model name provided: {model_name}. Please choose from {model_name_list}"
            )

        self.model_name = model_name
        self.api_key = os.getenv("OPENAI_API_KEY")

    def get_repaired_response(self, prompt: Prompt) -> str:
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

        if repaired_code:
            return repaired_code
        else:
            raise ValueError("No response.")
    
    def __str__(self):
        if self.model_name == "gpt-3.5-turbo-0125":
            return "gpt35"
        else:
            return "gpt4"


class GeminiApi(LlmApi):
    def __init__(self, model_name: MODEL_NAME) -> None:
        model_name_list = ["gemini-1.0-pro"]
        if not model_name in model_name_list:
            raise ValueError(
                f"Invalid model name provided: {model_name}. Please choose from {model_name_list}"
            )

        self.model_name = model_name
        self.api_key = os.getenv("GOOGLE_API_KEY")
        genai.configure(api_key=self.api_key, transport="rest")

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

    def get_repaired_response(self, prompt: Prompt):
        generation_config, safety_settings = self.get_config()

        model = genai.GenerativeModel(
            model_name=self.model_name,
            generation_config=generation_config,
            safety_settings=safety_settings,
        )

        convo = model.start_chat()
        convo.send_message(prompt.prompt)

        return convo.last.text

    def __str__(self):
        return "gemini"

class ClaudeApi(LlmApi):
    def __init__(self, model_name: MODEL_NAME) -> None:
        model_name_list = ["claude-3-opus-20240229"]
        if not model_name in model_name_list:
            raise ValueError(
                f"Invalid model name provided: {model_name}. Please choose from {model_name_list}"
            )

        self.model_name = model_name
        self.api_key = os.getenv("CLAUDE_API_KEY")
        self.client = Anthropic(
            # defaults to os.environ.get("ANTHROPIC_API_KEY")
            api_key=self.api_key,
        )

    def get_repaired_response(self, prompt: Prompt):
        message = self.client.messages.create(
            model=self.model_name,
            max_tokens=1000,
            temperature=0.9,
            messages=[
                {
                    "role": "user",
                    "content": [{"type": "text", "text": prompt.prompt}],
                }
            ],
        )

        return message.content[0].text
    
    def __str__(self):
        return "claude"


if __name__ == "__main__":
    dataset = QuixBugsDataset("python")
    prompt = Prompt(dataset[0])

    # model_name: MODEL_NAME = "gpt-3.5-turbo-0125"
    # a = OpenAiApi(model_name)

    # model_name: MODEL_NAME = "gemini-1.0-pro"
    # a = GeminiApi(model_name)

    # model_name: MODEL_NAME = "claude-3-opus-20240229"
    # a = ClaudeApi(model_name)

    # b = a.api_call(prompt)

    # print(b)

    # patch_group = a.get_patch_group(prompt)

    # print(patch_group)

    # with open("temp.json", "w") as f:
    #     f.write(patch_group.to_json())
