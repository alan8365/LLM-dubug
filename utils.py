import os
import re
import shutil
from glob import glob
from pathlib import Path
from typing import List, TypedDict


class TestInfo(TypedDict):
    function_name: str
    test_text: str
    test_result: str
    fail_test_case: List[int]


def extract_def_function(code: str):
    # function to extract def function block from py file
    def_block = []

    code = code.split("\n")
    for line in code:
        if line.startswith("def"):
            def_block.append(line)

    return def_block


def copy_to_custom_folder(generated_code_path: Path, index: int) -> None:
    """
    Copy generated code to a custom folder.

    Args:
        generated_code_path: Path to the generated code directory.
        index: Index of the generated code.

    Returns:
        None
    """
    # Set the destination path
    custom_folder_path = Path('datasets/QuixBugs/custom_python_programs')

    # Clean the file in dst folder if it exists
    if custom_folder_path.exists():
        shutil.rmtree(custom_folder_path)

    # Create the dst folder
    custom_folder_path.mkdir()

    # Get all the folders in the generated code path
    all_folders = os.listdir(generated_code_path)

    # Exclude folders starting with '.'
    all_folders = [folder for folder in all_folders if not folder.startswith('.')]

    # Sort the folders
    all_folders = sorted(all_folders)

    # Copy the generated code to custom folder
    for folder in all_folders:
        source_file = generated_code_path / folder / f'{folder}_{index}.py'
        destination_file = custom_folder_path / f'{folder}.py'
        shutil.copyfile(source_file, destination_file)


def get_all_function():
    function_list = glob('datasets/QuixBugs/python_programs/*.py')
    function_list = [Path(x).stem for x in function_list if not re.match(r'.*test.py', x) and 'node' not in x]
    function_list = sorted(function_list)

    return function_list


def extract_test_info_from_pytest_log(pytest_log: str) -> TestInfo:
    """
    Extracts test information from pytest log.

    Parameters:
    - pytest_log (str): The pytest log to extract test information from.

    Returns:
    - result (list): A list of dictionaries containing test information.
      Each dictionary contains the following keys:
        - 'function_name' (str): The name of the function.
        - 'test_text' (str): The test text.
        - 'test_result' (str): The result of the test ('pass' or 'fail').
        - 'fail_test_case' (list): A list of indices where the test failed.
    """

    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', re.VERBOSE)
    progress_text = re.compile(r'\[[\s\d]+%\]')
    text_divide = re.compile(r'(datasets/QuixBugs/python_testcases/test_(\w+).py) \s+ ([.Fs]+)', re.VERBOSE)

    output = pytest_log
    output = ansi_escape.sub('', output)
    output = progress_text.sub('', output)

    start_text = re.compile(r'.*=+ test session starts =+.*')
    start_index = start_text.search(output).start()

    end_text = re.compile(r'=+.* FAILURES =+.*')
    end_index = end_text.search(output).end()

    splitted_output = output[start_index:end_index]
    splitted_output = splitted_output.split('\n')
    splitted_output = splitted_output[6:-2]

    temp = []
    for i in range(len(splitted_output)):
        line = splitted_output[i]
        if line.startswith('datasets/QuixBugs/python_testcases/'):
            temp.append(line)
        else:
            temp[-1] = temp[-1].strip() + line.strip()
    splitted_output = temp

    parsed_output = splitted_output
    parsed_output = [text_divide.match(line).groups() for line in parsed_output]

    pass_count = 0
    fail_count = 0
    skip_count = 0
    result = []
    for _, function_name, text in parsed_output:
        pass_count += text.count('.')
        fail_count += text.count('F')
        skip_count += text.count('s')

        result.append({
            'function_name': function_name,
            'test_text': text,
            'test_result': 'pass' if text.count('F') == 0 else 'fail',
            'fail_test_case': [m.start() for m in re.finditer('F', text)]
        })

    observe_count = (fail_count, pass_count, skip_count)
    real_count_pattern = re.compile(r'=+ \s (\d+) \s failed, \s (\d+) \s passed, \s (\d+) \s skipped', re.VERBOSE)
    real_count = tuple(map(int, real_count_pattern.match(output.split('\n')[-2]).groups()))

    if real_count != observe_count:
        raise ValueError(f'Count number mismatched, real: {real_count}, observe: {observe_count}')

    return result
