def flatten(arr):
    for x in arr:
        if isinstance(x, list):
            for y in flatten(x):
                yield y
        else:
            yield x

# Testing the fixed code
arr = [1, [2, 3], [4, [5, 6]]]
print(list(flatten(arr)))  # Output: [1, 2, 3, 4, 5, 6]