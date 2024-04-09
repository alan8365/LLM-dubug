import os
import json
from pathlib import Path

from tqdm import tqdm  # type: ignore

from api import LlmApi, OpenAiApi, GeminiApi, ClaudeApi
from prompt import Prompt
from quixbugs import QuixBugsDataset
from src_types import LANG, PROMPT_TYPE


class Experiment:
    def __init__(
        self, name: str, lang: LANG, llm_api: LlmApi, prompt_type: PROMPT_TYPE = "basic"
    ) -> None:
        self.name = name
        self.lang = lang
        self.llm_api = llm_api
        self.prompt_type = prompt_type

        base_dir = Path(str(os.getenv("EXPS_DIR")))
        self.exp_dir = base_dir / self.name
        self.patch_dir = self.exp_dir / "patchs"
        exp_info_path = self.exp_dir / "exp_info.json"

        if not self.exp_dir.exists():
            # Make exp dir
            self.exp_dir.mkdir()

            # Make patchs dir
            self.patch_dir.mkdir()

            # Write the exp info
            with open(exp_info_path, "w") as f:
                f.write(self.to_json())

    def run(self):
        dataset = QuixBugsDataset(self.lang)
        # Count exist patch to skip them
        exist_patch_num = len(list(self.patch_dir.glob("*.json")))

        for i, sample in enumerate(tqdm(dataset)):
            if i < exist_patch_num:
                continue

            prompt = Prompt(sample, self.prompt_type)
            patch_group = self.llm_api.get_patch_group(prompt)

            json_path = self.patch_dir / f"{sample.prog_id}. {sample.prog_name}.json"
            with open(json_path, "w") as f:
                f.write(patch_group.to_json())

    def to_dict(self):
        return {
            "name": self.name,
            "lang": self.lang,
            "llm_api": self.llm_api.__class__.__name__,
            "prompt_type": self.prompt_type,
            "exp_dir": str(self.exp_dir),
            "patch_dir": str(self.patch_dir),
        }

    def to_json(self):
        return json.dumps(self.to_dict(), indent=4)


if __name__ == "__main__":
    exp = Experiment(
        "gpt35-python-with_step", "python", OpenAiApi("gpt-3.5-turbo-0125"), "with_step"
    )
    # exp = Experiment(
    #     "gpt4-python-with_lib_v2", "python", OpenAiApi("gpt-4"), "with_lib"
    # )
    # exp = Experiment(
    #     "gemini-python-with_step", "python", GeminiApi("gemini-1.0-pro"), "with_step"
    # )
    # exp = Experiment(
    #     "claude-python-basic", "python", ClaudeApi("claude-3-opus-20240229"), "basic"
    # )
    exp.run()
