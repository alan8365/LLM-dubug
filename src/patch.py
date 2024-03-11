from quixbugs import QuixBugsSample
from prompt import Prompt
from src_types import MODEL_NAME

from typing import Final, Optional
import json

PATCH_NUM_IN_GROUP: Final[int] = 3


class Patch:
    def __init__(
        self, patch_id: int, repaired_code: Optional[str], run_time: float
    ) -> None:
        # Patch data
        self.patch_id = patch_id
        self.repaired_code = repaired_code

        # Eval data
        self.run_time = run_time

    def __repr__(self) -> str:
        return f"Patch(id={self.patch_id}, run_time={self.run_time:.3f} s, repaired_code={self.repaired_code})"

    def to_json(self) -> str:
        patch_data = {
            "patch_id": self.patch_id,
            "run_time": self.run_time,
            "repaired_code": self.repaired_code,
        }
        return json.dumps(patch_data)


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


    def to_json(self):
        patchs_data = [
            {
                "patch_id": patch.patch_id,
                "run_time": patch.run_time,
                "repaired_code": patch.repaired_code,
            }
            for patch in self.patchs
        ]

        result = {
            "model_name": self.model_name,
            "prompt": self.prompt.prompt,
            "sample": self.prompt.sample.to_json(),
            "patches": patchs_data
        }

        return json.dumps(result, indent=4)
