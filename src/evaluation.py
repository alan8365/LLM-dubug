import os
import re
import json
import subprocess
from glob import glob
from pathlib import Path

import pytest
from tqdm import tqdm  # type: ignore

from patch import read_patch_group_from_json, PatchGroup, Patch
from quixbugs import QuixBugsSample
from prompt import Prompt
from src_types import LANG


class PatchGroupEvaluation:
    def __init__(self, patch_group: PatchGroup) -> None:
        self.patch_group = patch_group

        pytester = QuixBugsPytester(patch_group)
        self.test_result = pytester.test_result

    def to_dict(self):
        return {
            "sample": self.patch_group.sample.to_dict(),
            "patchs_eval": [
                {
                    "run_time": patch.run_time,
                    "pass_num": self.test_result[patch.patch_id]["pass_num"],
                    "fail_num": self.test_result[patch.patch_id]["fail_num"],
                    "reparied_code": self.test_result[patch.patch_id]["repaired_code"],
                }
                for patch in self.patch_group.patchs
            ],
        }


class ExperimentEvaluation:
    base_dir = Path(str(os.getenv("EXPS_DIR")))

    def __init__(self, exp_name: str) -> None:
        self.exp_dir = self.base_dir / exp_name
        self.patch_dir = self.exp_dir / "patchs"
        self.eval_dir = self.exp_dir / "evals"

        if not self.eval_dir.exists():
            self.eval_dir.mkdir()

        all_patch_path = list(self.patch_dir.glob("*.json"))
        all_patch_path = sorted(all_patch_path, key=lambda s: int(s.name.split(".")[0]))

        self.patch_groups = [
            read_patch_group_from_json(patch_path) for patch_path in all_patch_path
        ]

        for patch_group in tqdm(self.patch_groups):
            eval_patch_group = PatchGroupEvaluation(patch_group)

            prog_id = patch_group.sample.prog_id
            prog_name = patch_group.sample.prog_name
            with open(self.eval_dir / f"{prog_id}. {prog_name}.json", "w") as f:
                json.dump(eval_patch_group.to_dict(), f)

    def run(self):
        pass

    def plausible_check(self):
        pass

    def correct_check(self):
        pass

    def fault_localization(self):
        pass

    def to_dict(self):
        return {"patchs"}


class QuixBugsPytester:
    custom_dir = Path(str(os.getenv("QUIX_BUGS_DIR"))) / "custom_python_programs"

    def __init__(self, patch_group: PatchGroup):
        self.patch_group = patch_group
        self.sample = patch_group.sample

        self.test_path = self.sample.get_test_path()
        self.prog_name = self.sample.prog_name

        self.test_result: dict[int, dict] = {}
        for patch in self.patch_group.patchs:
            repaired_code = self.clean_response(patch.raw_code)
            pytest_log = self.validate_patch(repaired_code)
            test_info = self.get_test_info(pytest_log)
            test_info.update(
                {"repaired_code": repaired_code}
            )

            self.test_result[patch.patch_id] = test_info 

    def clean_response(self, response) -> str:
        lang = self.sample.language

        pattern = re.compile(rf"```{lang}=?(.*?)\n```", re.MULTILINE | re.DOTALL)
        find_all = pattern.findall(response)

        if find_all:
            cleaned_code = find_all[-1]
        else:
            raise ValueError(f"Pattern error:\n {response}")

        return cleaned_code

    def validate_patch(self, repaired_code: str):
        with open(self.custom_dir / f"{self.prog_name}.py", "w") as f:
            f.write(repaired_code)

        proc = subprocess.Popen(
            [
                "pytest",
                "--custom",
                str(self.test_path),
            ],
            stdout=subprocess.PIPE,
        )
        stdout = proc.stdout
        if stdout:
            output = stdout.read().decode("utf-8")

        return output

    def get_test_info(self, pytest_log: str):
        pattern = rf"test_{self.prog_name}\.py ([.Fs]*)"
        text_divide = re.compile(pattern)
        parsed_output = text_divide.findall(pytest_log)[0]

        pass_count = parsed_output.count(".")
        fail_count = parsed_output.count("F")
        skip_count = parsed_output.count("s")

        return {
            "pass_num": pass_count,
            "fail_num": fail_count,
            "skip_num": skip_count,
        }


if __name__ == "__main__":
    # exp_name = "gpt35-python-basic"
    # exp_name = "gpt35-python-with_lib_v2"
    exp_name = "gpt35-python-with_step"
    # exp_name = "gpt4-python-basic"
    # exp_name = "gpt4-python-with_lib_v2"
    # exp_name = "gemini-python-basic"
    # exp_name = "gemini-python-with_lib_v2"
    # exp_name = "gemini-python-with_step"
    # exp_name = "claude-python-basic"

    print(exp_name)
    eval = ExperimentEvaluation(exp_name)

    # exp_names = [i.name for i in ExperimentEvaluation.base_dir.glob("*")]
    # exp_names = sorted(exp_names)
    # for exp_name in exp_names[4:]:
    #     print(exp_name)
    #     eval = ExperimentEvaluation(exp_name)
