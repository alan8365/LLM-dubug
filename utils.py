def extract_def_function(code: str):
    # function to extract def function block from py file
    def_block = []

    code = code.split("\n")
    for line in code:
        if line.startswith("def"):
            def_block.append(line)


    return def_block


if __name__ == '__main__':
    with open("main.py", "r") as f:
        test_code = f.read()

    extract_def_function(test_code)
