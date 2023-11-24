def max_sublist_sum(arr):
    max_ending_here = 0
    max_so_far = 0

    for x in arr:
        max_ending_here = max(x, max_ending_here + x) # fix: consider the current element or the sum of the current element and the previous sum
        max_so_far = max(max_so_far, max_ending_here)

    return max_so_far