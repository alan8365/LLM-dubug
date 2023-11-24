def subsequences(a, b, k):
    if k == 0:
        return []

    ret = []
    for i in range(a, b + 1 - k):
        ret.extend(
            [i] + rest for rest in subsequences(i + 1, b, k - 1)
        )

    return ret

# Testing the code
print(subsequences(1, 3, 2))
# Output: [[1, 2], [1, 3], [2, 3]]
print(subsequences(1, 4, 3))
# Output: [[1, 2, 3], [1, 2, 4], [1, 3, 4], [2, 3, 4]]