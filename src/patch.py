from quixbugs import QuixBugsSample
from prompt import Prompt
from src_types import MODEL_NAME

from typing import Final, Optional

PATCH_NUM_IN_GROUP: Final[int] = 3


# TODO complete this
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

        # Bug data
        self.sample = prompt.sample

        # LLM data
        self.prompt = prompt
        self.model_name = model_name
