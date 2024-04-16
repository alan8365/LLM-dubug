import tokenize
import io

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
            out += (" " * (start_col - last_col))
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
    lines = source.split('\n')
    
    # Remove trailing whitespace from each line
    cleaned_lines = [line.rstrip() for line in lines]
    cleaned_lines = [line for line in cleaned_lines if line != '']

    return '\n'.join(cleaned_lines)

def cleaning_code(source: str) -> str:
    comments_removed = remove_comments(source)
    whitespace_removed = remove_trailing_whitespace(comments_removed)

    return whitespace_removed.strip()

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