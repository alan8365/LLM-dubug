from typing import Literal, Optional

from dotenv import load_dotenv
from pathlib import Path

import os
import json

load_dotenv()

LANG = Literal["python", "java"]
CODE_TYPE = Literal["buggy", "correct", "testcase"]
LIB = Literal["Node", "WeightedEdge"]

class QuixBugsDatasetItem:
    def __init__(
        self,
        prog_id: int,
        prog_name: str,
        language: LANG,
        base_dir: Optional[str] = None,
    ) -> None:
        self.prog_id = prog_id
        self.prog_name = prog_name
        self.language = language

        if self.language not in ["python", "java"]:
            raise ValueError(f"Unsupported language: {self.language}")

        if base_dir:
            self.base_dir = Path(base_dir)
        elif os.getenv("QUIX_BUGS_DIR"):
            self.base_dir = Path(str(os.getenv("QUIX_BUGS_DIR")))

        self.buggy_code = self.read_code("buggy")
        self.correct_code = self.read_code("correct")

        self.lib_usage: dict[LIB, str] = self.detect_library_usage()
        # TODO add bug type here
        # self.bug_type = bug_type

    def get_code_path(self, code_type: CODE_TYPE) -> Path:
        """
        This method returns the code file path based on the code type and language.
        It constructs the file path using the base directory, program directory, and file name.
        If the file path does not exist, it raises a FileNotFoundError.

        Args:
            code_type (CODE_TYPE): The type of the code ('buggy', 'correct', 'testcase').

        Returns:
            Path: The file path.
        """
        if code_type == "testcase":
            raise ValueError("Code type cannot be 'testcase'")

        # Example: correct dir for python - "correct_python_programs"
        # Example: buggy dir for python   - "python_programs"
        prog_dir_prefix = "" if code_type == "buggy" else "correct_"

        prog_dir_name = f"{prog_dir_prefix}{self.language}_programs"
        prog_dir = self.base_dir / prog_dir_name

        if self.language == "python":
            # Example: bitcount.py
            filename = f"{self.prog_name}.py"
        elif self.language == "java":
            # Example: BITCOUNT.java
            filename = f"{self.prog_name.upper()}.java"

        file_path = prog_dir / filename

        if not file_path.exists():
            raise FileNotFoundError(f"File {file_path} does not exist")

        return file_path

    def get_test_path(self) -> Path:
        """
        This method returns the test file path based on the language.
        It constructs the file path using the base directory, test directory, and file name.
        If the file path does not exist, it raises a FileNotFoundError.

        Returns:
            Path: The test file path.
        """

        # Example: python_testcases
        testcase_dir = self.base_dir / f"{self.language}_testcases"

        if self.language == "python":
            # Example: test_bitcount.py
            filename = f"test_{self.prog_name}.py"
        elif self.language == "java":
            # Example: BITCOUNT_TEST.java
            filename = f"{self.prog_name.upper()}_TEST.java"

        testcase_path = testcase_dir / filename

        return testcase_path

    def read_code(self, code_type: CODE_TYPE) -> str:
        """
        This method reads the code from the file path based on the code type.
        It uses the get_code_path method to get the file path.
        If the file path does not exist, it raises a FileNotFoundError.

        Args:
            code_type (CODE_TYPE): The type of code to read.

        Returns:
            str: The code content.
        """
        if code_type == "testcase":
            file_path = self.get_test_path()
        else:
            file_path = self.get_code_path(code_type)

        with open(file_path, "r") as f:
            file_content = f.read()

        return file_content

    def detect_library_usage(self) -> dict[LIB, str]:
        """
        This method detects the usage of libraries in the test file.
        It reads the test file content and checks for import statements of specific libraries.
        If the import statement is found, it retrieves the content of the library file.
        The result is a dictionary where the key is the library name and the value is the library content.
        If the test file does not exist, it returns an empty dictionary.

        Returns:
            dict: A dictionary where the key is the library name and the value is the library content.
        """
        try:
            test_content = self.read_code("testcase")
        except FileNotFoundError:
            test_content = ""

        import_statements: dict[LANG, dict[LIB, str]] = {
            "python": {"Node": "from node import Node"},
            "java": {
                "Node": "import java_programs.Node;",
                "WeightedEdge": "import java_programs.WeightedEdge;",
            },
        }

        import_statement = import_statements[self.language]

        result: dict[LIB, str] = {}
        for lib_name, lib_statement in import_statement.items():
            result[lib_name] = ""
            if lib_statement in test_content:
                result[lib_name] = self.get_lib_content(lib_name)

        return result

    def get_lib_path(self, lib_name: LIB) -> Path:
        """Retrieve the file path for a specific library.

        Args:
            lib_name (LIB): The name of the library.

        Returns:
            Path: The file path of the library.
        """

        if self.language == "python":
            # Example: node.py
            lib_file_name = f"{lib_name.lower()}.py"
        elif self.language == "java":
            # Example: Node.java
            lib_file_name = f"{lib_name}.java"

        lib_dir_name = f"{self.language}_programs"
        lib_file_path = self.base_dir / lib_dir_name / lib_file_name

        return lib_file_path

    def get_lib_content(self, lib_name: LIB) -> str:
        """Retrieve the content of a specific library.

        Args:
            lib_name (LIB): The name of the library.

        Returns:
            str: The content of the library.
        """

        lib_file_path = self.get_lib_path(lib_name)

        try:
            with open(lib_file_path, "r") as lib_file:
                return lib_file.read()
        except FileNotFoundError:
            print(f"Library file not found: {lib_file_path}")
            return ""

    def __repr__(self) -> str:
        return f"QuixBugsDatasetItem(ID: {self.prog_id}, Prog Name: {self.prog_name}, Language: {self.language})"


class QuixBugsDataset:
    def __init__(self):
        with open('prog_names.json', 'r') as file:
            self.prog_names = json.load(file)
        self.items: list[QuixBugsDatasetItem] = ''


if __name__ == "__main__":
    quixbugs_dataset_item = QuixBugsDatasetItem(0, "minimum_spanning_tree", "java")

    # print(quixbugs_dataset_item)

    a = quixbugs_dataset_item.get_lib_content("Node")
    # print(a)
