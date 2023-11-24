def is_valid_parenthesization(parens):
    depth = 0
    for paren in parens:
        if paren == '(':
            depth += 1
        else:
            if depth <= 0:
                return False
            depth -= 1

    return depth == 0