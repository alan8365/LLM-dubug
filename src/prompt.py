import json
from typing import Literal

from quixbugs import QuixBugsSample, QuixBugsDataset
from src_types import PROMPT_TYPE


class Prompt:
    prompt_templates: dict[PROMPT_TYPE, str] = {
        "basic": (
            "Fix the bugs in the following code:\n"
            "```{lang}=\n"
            "{code}\n"
            "```\n"
            "\n"
            "Fixed code:\n"
        ),
        "with_lib": (
            "Fix the bugs in the following code:\n"
            "```{lang}=\n"
            "{code}\n"
            "```\n"
            "Here is the library code used in the code above. The library is view-only and uneditable:\n"
            "```{lang}=\n"
            "{lib_code}\n"
            "```\n"
            "Fixed code:\n"
        ),
        "with_step": (
            "Your task involves two steps: First, identify the bug and its location in the provided code. Second, generate a patch to fix the code by replacing the section containing the bug. Lastly, provide the complete code with the patch applied.\n"
            "```{lang}=\n"
            "{code}\n"
            "```\n"
            "Here is the library code used in the code above. The library is view-only and uneditable:\n"
            "```{lang}=\n"
            "{lib_code}\n"
            "```\n"
        )
    }

    def __init__(
        self, sample: QuixBugsSample, prompt_type: PROMPT_TYPE = "basic"
    ) -> None:
        self.sample = sample
        self.prompt_type = prompt_type

        lib_code = "\n".join(sample.lib_usage.values())
        prompt = self.prompt_templates[prompt_type].format(
            lang=sample.language, code=sample.buggy_code, lib_code=lib_code
        )

        self.prompt = prompt

    def __repr__(self) -> str:
        return f"Prompt(prompt type: {self.prompt_type}, sample: {self.sample})"

    def to_dict(self) -> dict:
        return {
            "prompt": self.prompt,
            "sample": self.sample.to_dict(),
            "prompt_type": self.prompt_type,
        }

    def to_json(self) -> str:
        return json.dumps(
            self.to_dict,
            indent=4,
        )


if __name__ == "__main__":
    a = QuixBugsDataset("python")
    b = a["breadth_first_search"]
    c = Prompt(b, "basic")

    print(c.prompt)
