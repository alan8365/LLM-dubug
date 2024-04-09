from quixbugs import QuixBugsSample, QuixBugsDataset
from prompt import Prompt
from src_types import MODEL_NAME, LANG, PROMPT_TYPE

from typing import Final, Optional
import json

PATCH_NUM_IN_GROUP: Final[int] = 3


class Patch:
    def __init__(
        self,
        patch_id: int,
        raw_code: str,
        repaired_code: str,
        run_time: float,
    ) -> None:
        # Patch data
        self.patch_id = patch_id
        self.repaired_code = repaired_code
        self.raw_code = raw_code

        # Eval data
        self.run_time = run_time

    def __repr__(self) -> str:
        return f"Patch(id={self.patch_id}, run_time={self.run_time:.3f} s, repaired_code={self.repaired_code})"

    def to_dict(self) -> dict:
        return {
            "patch_id": self.patch_id,
            "run_time": self.run_time,
            "repaired_code": self.repaired_code,
            "raw_code": self.raw_code,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict)


class PatchGroup:
    def __init__(
        self,
        patchs: list[Patch],
        prompt: Prompt,
        model_name: MODEL_NAME,
    ) -> None:
        if not len(patchs) == PATCH_NUM_IN_GROUP:
            raise ValueError(
                f"Incorrect number of patches in the group: {len(patchs)}, expected {PATCH_NUM_IN_GROUP}"
            )

        self.patchs = patchs

        # Bug data
        self.sample = prompt.sample

        # LLM data
        self.prompt = prompt
        self.model_name = model_name

    def __getitem__(self, index: int) -> Patch:
        return self.patchs[index]

    def __repr__(self):
        return f"PatchGroup(model name: {self.model_name}, prompt: {self.prompt})"

    def to_dict(self):
        patchs_data = [patch.to_dict() for patch in self.patchs]

        return {
            "model_name": self.model_name,
            "prompt": self.prompt.to_dict(),
            "patches": patchs_data,
        }

    def to_json(self):
        return json.dumps(self.to_dict(), indent=4)


# TODO complete this func
def read_patch_group_from_json(file_path) -> PatchGroup:
    with open(file_path, "r") as f:
        json_data = json.load(f)

    lang: LANG = json_data["prompt"]["sample"]["language"]
    model_name: MODEL_NAME = json_data["model_name"]
    prompt_type: PROMPT_TYPE = json_data["prompt"]["prompt_type"]
    prog_id: int = json_data["prompt"]["sample"]["prog_id"]

    dataset = QuixBugsDataset(lang)
    prompt = Prompt(dataset[prog_id], prompt_type)

    patches = []
    for i in range(3):
        patch = json_data["patches"][i]

        raw_code = patch["raw_code"]
        repaired_code = patch["repaired_code"]
        run_time = patch["run_time"]
        patches.append(Patch(i, raw_code, repaired_code, run_time))

    return PatchGroup(patches, prompt, model_name)
