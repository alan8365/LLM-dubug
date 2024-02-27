from typing import Literal 

from dotenv import load_dotenv
from pathlib import Path

import os

load_dotenv()

# - QuixBugs dataset item schema
#   - ID
#   - Bug data
#     - Prog name
#     - Language
#     - Lib usage
#     - Bug type
#   - Code data
#     - Buggy code
#     - Correct code

LANG = Literal['python', 'java'] 
CODE_TYPE = Literal['buggy', 'correct', 'testcase']

class QuixBugsDatasetItem:
    def __init__(self, prog_id: int, prog_name: LANG, language: str) -> None:
        self.prog_id = prog_id
        self.prog_name = prog_name
        self.language = language

        if self.language not in ['python', 'java']:
            raise ValueError(f"Unsupported language: {self.language}")
        
        self.base_dir = Path(os.getenv("QUIX_BUGS_DIR")) 

        self.buggy_code = self.read_code('buggy')
        self.correct_code = self.read_code('correct')

        self.testcase_code = self.read_code('testcase')
        print(self.testcase_code)

        # self.lib_usage = lib_usage
        # self.bug_type = bug_type

    def get_file_path(self, code_type: CODE_TYPE) -> str:
        prog_dir_prefix = '' if code_type == 'buggy' else 'correct_'

        prog_dir_name = f'{prog_dir_prefix}{self.language}_programs'
        prog_dir = self.base_dir / prog_dir_name

        if self.language == 'python':
            filename = f'{self.prog_name}.py'
        elif self.language == 'java': 
            filename = f'{self.prog_name.upper()}.java'

        file_path = prog_dir / filename

        if not file_path.exists():
            raise FileNotFoundError(f"File {file_path} does not exist")

        return file_path
    
    def get_test_path(self):
        testcase_dir = self.base_dir / f'{self.language}_testcases'

        if self.language == 'python':
            filename = f'test_{self.prog_name}.py'
        elif self.language == 'java':
            filename = f'{self.prog_name.upper()}_TEST.java'
            
        testcase_path = testcase_dir / filename

        return testcase_path

    def read_code(self, code_type: CODE_TYPE) -> str:
        if code_type == 'testcase':
            file_path = self.get_test_path()
        else:
            file_path = self.get_file_path(code_type)

        with open(file_path, 'r') as f:
            file_content = f.read() 

        return file_content

    def detect_library_usage(self, test_path, lib_name, language):
        if not os.path.exists(test_path):
            return False

        import_statements = {
            "Node": {
                "Python": "from node import Node",
                "Java": "import java_programs.Node;"
            },
            "WeightedEdge": {
                "Java": "import java_programs.WeightedEdge;"
            }
        }
        import_statement = import_statements[lib_name].get(language, "")
        if import_statement:
            with open(test_path, 'r') as test_file:
                test_content = test_file.read()
            return import_statement in test_content

        return False

class QuixBugsDataset:
    def __init__(self, items: list[QuixBugsDatasetItem]):
        self.items = items


if __name__ == "__main__":
    quixbugs_dataset_item = QuixBugsDatasetItem(
        0,
        'bitcount',
        'python'
    )

