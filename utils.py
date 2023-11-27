import os
import re
import shutil
from glob import glob
from pathlib import Path


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
