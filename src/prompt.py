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
            "Here is the library code used in the code above:\n"
            "```{lang}=\n"
            "{lib_code}\n"
            "```\n"
            "Fixed code:\n"
        ),
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

    def __repr__(self):
        return f"Prompt(prompt type: {self.prompt_type}, sample: {self.sample})"



if __name__ == "__main__":
    a = QuixBugsDataset("python")
    b = a["breadth_first_search"]
    c = Prompt(b, "basic")

    print(c.prompt)
