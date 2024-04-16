from dotenv import load_dotenv

from src_types import LANG, CODE_TYPE, LIB


from typing import Optional, Union
from pathlib import Path
import os
import json
import re

load_dotenv()


class QuixBugsSample:
    """A class representing an item in the QuixBugs dataset."""

    def __init__(
        self,
        prog_info: dict,
        language: LANG,
        base_dir: Optional[Path] = None,
    ) -> None:
        self.prog_id = prog_info["prog_id"]
        self.prog_name = prog_info["prog_name"]
        self.language = language

        if self.language not in ["python", "java"]:
            raise ValueError(f"Unsupported language: {self.language}")

        if base_dir:
            self.base_dir = base_dir
        elif os.getenv("QUIX_BUGS_DIR"):
            self.base_dir = Path(str(os.getenv("QUIX_BUGS_DIR")))

        self.org_buggy_code = self.read_code("buggy")
        self.buggy_code = self.delete_comment(self.org_buggy_code)
        self.correct_code = self.read_code("correct")
        self.correct_code = self.delete_comment(self.correct_code)

        self.lib_usage: dict[LIB, str] = self.detect_library_usage()

        self.bug_type = prog_info["bug_type"]
        self.bug_detail_desc = prog_info["bug_detail_desc"]
        self.fault_location = prog_info["fault_location"]
        self.testcase_num = prog_info["testcase_num"]

    def get_code_path(self, code_type: CODE_TYPE) -> Path:
        """
        This method returns the code file path based on the code type and language.
        It constructs the file path using the base directory, program directory, and file name.
        If the file path does not exist, it raises a FileNotFoundError.

        Args:
            code_type (CODE_TYPE): The type of the code ('buggy', 'correct').

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

    def get_testcase_json(self) -> list:
        testcase_dir = self.base_dir / f"json_testcases"
        json_path = testcase_dir / f"{self.prog_name}.json"

        if json_path.exists():
            with open(testcase_dir / f"{self.prog_name}.json") as f:
                result = [json.loads(line) for line in f.readlines()]
        else:
            result = []

        return result

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

    def delete_comment(self, code: str):
        if self.language == "python":
            pattern = re.compile(r"\"{3}.*?\"{3}", re.MULTILINE | re.DOTALL)

            pure_code = pattern.sub("", code)
        elif self.language == "java":
            pattern = re.compile(r"/\*.*?\*/", re.MULTILINE | re.DOTALL)
            pure_code = pattern.sub("", code)

        return pure_code

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
        return f"QuixBugsSample(ID: {self.prog_id}, Language: {self.language}, Prog Name: {self.prog_name})"

    def to_dict(self) -> dict:
        return {
            "prog_id": self.prog_id,
            "prog_name": self.prog_name,
            "language": self.language,
            "testcase_num": self.testcase_num,
            "fault_location": self.fault_location,
            "bug_type": self.bug_type,
            "bug_detail_desc": self.bug_detail_desc,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=4)


class QuixBugsDataset:
    """A class representing a dataset of QuixBugs programs."""

    def __init__(self, langauge: LANG):
        self.base_dir = Path(str(os.getenv("QUIX_BUGS_DIR")))
        with open(self.base_dir / "prog_info.json", "r") as file:
            self.prog_info: list[dict] = json.load(file)
        self.prog_names = [i["prog_name"] for i in self.prog_info]

        self.prog_names_dict = {
            prog_name: i for i, prog_name in enumerate(self.prog_names)
        }
        self.items: list[QuixBugsSample] = [
            QuixBugsSample(
                prog,
                langauge,
                self.base_dir,
            )
            for prog in self.prog_info
        ]

    def __len__(self):
        return len(self.items)

    def __getitem__(self, index: Union[int, str]) -> QuixBugsSample:
        if isinstance(index, int):
            return self.items[index]
        elif isinstance(index, str):
            i = self.prog_names_dict[index]

            return self.items[i]
        else:
            raise ValueError(
                f"Invalid index type: {type(index)}. Index must be int or str."
            )

    def __iter__(self):
        yield from self.items


if __name__ == "__main__":
    quix_bugs_dataset = QuixBugsDataset("python")

    for i in quix_bugs_dataset:
        print(i)
        print(i.testcase_num)

    # a = []
    # for i in quix_bugs_dataset:
    #     a.append(
    #         {
    #             "prog_id": i.prog_id,
    #             "prog_name": i.prog_name,
    #             "fault_location": i.fault_location,
    #             "bug_type": i.bug_type,
    #             "testcase_num": i.testcase_num,
    #         }
    #     )

    # with open("prog_info.json", "w") as f:
    #     json.dump(a, f)
