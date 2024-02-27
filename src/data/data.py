import os


def read_files_content(buggy_path, correct_path):
    with open(buggy_path, 'r') as buggy_file, open(correct_path, 'r') as correct_file:
        return buggy_file.read(), correct_file.read()

class DataModule:
    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.data = []
        self.excluded_files = ['Node.java', 'node.py', 'WeightedEdge.java']
        self.dirs = {
            "Python": ("Python", ".py", 
                       "python_programs", 
                       "correct_python_programs", 
                       "python_testcases"),
            "Java": ("Java", ".java", 
                     "java_programs", 
                     "correct_java_programs", 
                     "java_testcases")
        }
        self.traverse_and_pair_directories()

    def traverse_and_pair_directories(self):
        for language, ext, buggy_dir, correct_dir, test_dir in self.dirs.values():
            full_buggy_dir = os.path.join(self.base_dir, buggy_dir)
            full_correct_dir = os.path.join(self.base_dir, correct_dir)
            full_test_dir = os.path.join(self.base_dir, test_dir)
        
            self.pair_code(full_buggy_dir, full_correct_dir, full_test_dir, language, ext)

    def pair_code(self, buggy_dir, correct_dir, test_dir, language, ext):
        for file_name in os.listdir(buggy_dir):
            if self.is_valid_file(file_name, ext):
                buggy_path, correct_path, test_path = self.get_file_paths(buggy_dir, correct_dir, test_dir, file_name,
                                                                          language)
                buggy_code, correct_code = read_files_content(buggy_path, correct_path)
                uses_node_lib = self.detect_library_usage(test_path, "Node", language)
                uses_weighted_edge_lib = self.detect_library_usage(test_path, "WeightedEdge", language)

                base_file_name = os.path.splitext(file_name)[0].lower()

                self.data.append({
                    "language": language,
                    "file_name": base_file_name,
                    "buggy_code": buggy_code,
                    "correct_code": correct_code,
                    "annotations": {
                        "uses_node_lib": uses_node_lib,
                        "uses_weighted_edge_lib": uses_weighted_edge_lib
                    }
                })

    def is_valid_file(self, file_name, ext):
        """
        Determines if a file should be included in the dataset.

        Args:
        file_name (str): The name of the file.
        ext (str): The expected file extension.

        Returns:
        bool: True if the file should be included, False otherwise.
        """
        if file_name in self.excluded_files:
            return False

        # Exclude files ending with 'test.py'
        if file_name.endswith('test.py'):
            return False

        # Include files with the correct extension
        return file_name.endswith(ext)

    def get_file_paths(self, buggy_dir, correct_dir, test_dir, file_name, language):
        buggy_path = os.path.join(buggy_dir, file_name)
        correct_path = os.path.join(correct_dir, file_name)

        file_name = os.path.splitext(file_name)[0]
        test_file_name = f"test_{file_name}.py" if language == "Python" else f"{file_name}_TEST.java"
        test_path = os.path.join(test_dir, test_file_name)
        return buggy_path, correct_path, test_path

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

    def get_lib_content(self, lang: str, lib_name: str) -> str:
        """
        Retrieves the content of a library file based on the language and library name.

        Args:
        lang (str): The programming language of the library ('Python' or 'Java').
        lib_name (str): The name of the library.

        Returns:
        str: The content of the library file, or an empty string if the file is not found.
        """
        lib_dir = self.dirs.get(lang, [])

        if not lib_dir:
            return ""  # Return empty if language directory is not defined

        if lang == "Python":
            lib_file_name = f"{lib_name}.py"
        elif lang == "Java":
            lib_file_name = f"{lib_name}.java"
        else:
            raise ValueError(f"Invalid language: {lang}")

        lib_file_path = os.path.join(self.base_dir, lib_dir[2], lib_file_name)

        try:
            with open(lib_file_path, 'r') as lib_file:
                return lib_file.read()
        except FileNotFoundError:
            print(f"Library file not found: {lib_file_path}")
            return ""

    def get_data(self):
        return self.data


if __name__ == "__main__":
    data_module = DataModule("../../datasets/QuixBugs")
    data_module.traverse_and_pair_directories()
    processed_data = data_module.get_data()
    data_module.get_lib_content("Java", "Node")
    print(processed_data)
