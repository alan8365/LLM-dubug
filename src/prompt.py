import json
from typing import Literal

from quixbugs import QuixBugsSample, QuixBugsDataset
from src_types import PROMPT_TYPE


class Prompt:
    prompt_templates: dict[PROMPT_TYPE, str] = {
        "basic": (
            "Fix the bug in the following code:\n"
            "```{lang}=\n"
            "{code}\n"
            "```\n"
            "\n"
            "Fixed code:\n"
        ),
        "with_lib": (
            "Fix the bug in the following code:\n"
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
            "Fix the bug in the following code step by step and show the comepelte fixed code in the end of :\n"
            "```{lang}=\n"
            "{code}\n"
            "```\n"
            "Here is the library code used in the code above. The library is view-only and uneditable:\n"
            "```{lang}=\n"
            "{lib_code}\n"
            "```\n"
        ),
        "with_location": (
            "Fix the bug in the following code. The bug is on the line commented below:\n"
            "```{lang}=\n"
            "{code}\n"
            "```\n"
        ),
    }

    def __init__(
        self, sample: QuixBugsSample, prompt_type: PROMPT_TYPE = "basic"
    ) -> None:
        self.sample = sample
        self.prompt_type = prompt_type

        lib_code = "\n".join(sample.lib_usage.values()).strip()
        buggy_code = sample.buggy_code.strip()
        if prompt_type == "with_location":
            fault_location = int(sample.fault_location)

            buggy_code = sample.buggy_code.split("\n")
            buggy_code[fault_location] = (
                buggy_code[fault_location] + " # The bug is here"
            )
            buggy_code = "\n".join(buggy_code)

        prompt = self.prompt_templates[prompt_type].format(
            lang=sample.language, code=buggy_code, lib_code=lib_code
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

    with open("temp.md", "w") as f:
        for b in a:
            c = Prompt(b, "with_location")

            text = (
                f"## {b.prog_id}.{b.prog_name}\n"
                "\n"
                f"Bug detail: {b.bug_detail_desc}\n"
                "\n"
                "### Prompt\n"
                f"{c.prompt}\n"
            )

            f.write(text)

