def kth(arr, k):
    if len(arr) == 1:
        return arr[0]
    pivot = arr[0]
    below = [x for x in arr[1:] if x < pivot]
    above = [x for x in arr[1:] if x > pivot]

    num_less = len(below)
    num_lessoreq = len(arr) - len(above)

    if k < num_less:
        return kth(below, k)
    elif k >= num_lessoreq:
        return kth(above, k - num_lessoreq)
    else:
        return pivot