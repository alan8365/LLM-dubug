import tokenize
import io
import os
import re
import json

from pathlib import Path
from tokenize import TokenError
from black import format_str, FileMode
from typing import Literal


def remove_comments(source):
    """
    Removes comments and docstrings from a Python source file.
    """
    io_obj = io.StringIO(source)
    out = ""
    prev_toktype = tokenize.INDENT
    last_lineno = -1
    last_col = 0
    for tok in tokenize.generate_tokens(io_obj.readline):
        token_type = tok[0]
        token_string = tok[1]
        start_line, start_col = tok[2]
        end_line, end_col = tok[3]
        ltext = tok[4]
        # The following two conditions preserve indentation
        if start_line > last_lineno:
            last_col = 0
        if start_col > last_col:
            out += " " * (start_col - last_col)
        # Remove comments:
        if token_type == tokenize.COMMENT:
            pass
        elif token_type == tokenize.STRING:
            if prev_toktype != tokenize.INDENT:
                if prev_toktype != tokenize.NEWLINE:
                    if start_col > 0:
                        out += token_string
        else:
            out += token_string
        prev_toktype = token_type
        last_col = end_col
        last_lineno = end_line
    return out


def remove_trailing_whitespace(source: str):
    lines = source.split("\n")

    # Remove trailing whitespace from each line
    cleaned_lines = [line.rstrip() for line in lines]
    cleaned_lines = [line for line in cleaned_lines if line != ""]

    return "\n".join(cleaned_lines)


def cleaning_code(source: str) -> str:
    source = source.strip()
    try:
        comments_removed = remove_comments(source)
    except (TokenError, IndentationError):
        comments_removed = source
    whitespace_removed = remove_trailing_whitespace(comments_removed)
    formated = format_code(whitespace_removed)

    return formated.strip()


def format_code(source: str) -> str:
    formated_code = format_str(source, mode=FileMode())

    return formated_code


if __name__ == "__main__":
    source_code = """def kheapsort(arr, k):
    \"\"\"
    yield k-th smallest elements in the input one at a time.
    \"\"\"
    import heapq
    heap = []
    for x in arr:
        heapq.heappush(heap, -x)
        if len(heap) > k:
            heapq.heappop(heap)
    while heap:
        yield -heapq.heappop(heap)
    """

    clean_code = cleaning_code(source_code)
    print(clean_code)


def get_pass_ratio(patch_info):
    testcase_num = patch_info["sample"]["testcase_num"]
    patchs_eval = patch_info["patchs_eval"]

    pass_ratio = sum([i["pass_num"] for i in patchs_eval]) / (testcase_num * 3)

    return pass_ratio


def get_correct_ratio(patch_info):
    eval_values = patch_info["patchs_art_evals"].values()
    correct_ratio = [v["is_correct"] == "T" for v in eval_values]
    correct_ratio = sum(correct_ratio) / 3

    return correct_ratio


def calculate_ratio(
    exp_name: str, calc_type: Literal["plausible", "correct"]
) -> dict[str, float]:
    base_dir = Path(str(os.getenv("EXPS_DIR")))
    result = {}

    if calc_type == "plausible":
        eval_dir = base_dir / exp_name / "evals"
    elif calc_type == "correct":
        eval_dir = base_dir / exp_name / "evals_art"

    if not eval_dir.exists():
        return {}

    all_eval_path = list(eval_dir.glob("*"))
    all_eval_path = sorted(all_eval_path, key=lambda p: int(p.name.split(".")[0]))

    for eval_path in all_eval_path:
        with open(eval_path, "r") as f:
            patch_info = json.load(f)

        prog_name = patch_info["sample"]["prog_name"]

        if calc_type == "plausible":
            result[prog_name] = get_pass_ratio(patch_info)
        elif calc_type == "correct":
            result[prog_name] = get_correct_ratio(patch_info)

    return result
