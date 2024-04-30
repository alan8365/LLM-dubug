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
from utils import cleaning_code


class PatchGroupEvaluation:
    def __init__(self, patch_group: PatchGroup) -> None:
        self.patch_group = patch_group
        self.sample = patch_group.sample

        pytester = QuixBugsPytester(patch_group)
        self.test_result = pytester.test_result

    def to_dict(self):
        return {
            "sample": self.sample.to_dict(),
            "patchs_eval": [
                {
                    "run_time": patch.run_time,
                    "is_plausible": self.test_result[patch.patch_id]["is_plausible"],
                    "is_correct": self.test_result[patch.patch_id]["is_correct"],
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

    def run(self):
        for patch_group in tqdm(self.patch_groups):
            eval_patch_group = PatchGroupEvaluation(patch_group)

            prog_id = patch_group.sample.prog_id
            prog_name = patch_group.sample.prog_name
            with open(self.eval_dir / f"{prog_id}. {prog_name}.json", "w") as f:
                json.dump(eval_patch_group.to_dict(), f, indent=4, ensure_ascii=False)

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
            repaired_code = cleaning_code(repaired_code)
            pytest_log = self.validate_patch(repaired_code)
            test_info = self.get_test_info(pytest_log)

            is_plausible = self.plausible_check(test_info)
            is_correct = self.correct_check(repaired_code)

            test_info.update({"repaired_code": repaired_code})
            test_info.update({"is_plausible": is_plausible})
            test_info.update({"is_correct": is_correct})

            self.test_result[patch.patch_id] = test_info

    def clean_response(self, response) -> str:
        lang = self.sample.language
        prog_name = self.sample.prog_name

        pattern = re.compile(rf".*```{lang}=?(.*def {prog_name}.*?)\n```", re.MULTILINE | re.DOTALL)
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

        pass_compile = re.compile(r"=+.*?(\d+) passed.*?=+")
        fail_compile = re.compile(r"=+.*?(\d+) failed.*?=+")

        pass_match = pass_compile.search(pytest_log)
        fail_match = fail_compile.search(pytest_log)

        if pass_match:
            pass_count = int(pass_match.group(1))
        else:
            pass_count = 0

        if fail_match:
            fail_count = int(fail_match.group(1))
        else:
            fail_count = 0

        return {
            "pass_num": pass_count,
            "fail_num": fail_count,
        }

    def plausible_check(self, test_info: dict[str, int]):
        testcase_num = self.sample.testcase_num

        return test_info["pass_num"] == testcase_num

    def correct_check(self, repaired_code: str):
        correct_code = cleaning_code(self.sample.correct_code)

        return correct_code == repaired_code


if __name__ == "__main__":
    exp_names = [
        "gpt35-python-basic",
        "gpt35-python-with_lib_v2",
        "gpt35-python-with_location",
        "gpt35-python-with_location_v2",
        "gpt35-python-with_location_v3",
        "gpt35-python-with_step",
        "gpt4-python-basic",
        "gpt4-python-basic_v2",
        "gpt4-python-with_lib_v2",
        "gpt4-python-with_lib_v3",
        "gpt4-python-with_location",
        "gemini-python-basic",
        "gemini-python-with_lib_v2",
        "gemini-python-with_location",
        "gemini-python-with_location_v2",
        "gemini-python-with_location_v3",
        "gemini-python-with_step",
        "gemini-python-with_step_v2",
        "gemini-python-with_step_v3",
        "claude-python-basic",
    ]

    exp_name = exp_names[7]
    print(exp_name)

    eval = ExperimentEvaluation(exp_name)
    eval.run()

    # for exp_name in exp_names[-6:]:
    #     print(exp_name)
    #     eval = ExperimentEvaluation(exp_name)
    #     eval.run()
