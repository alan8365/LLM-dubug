def quicksort(arr):
    if len(arr) <= 1:
        return arr

    pivot = arr[0]
    lesser = [x for x in arr[1:] if x < pivot]
    greater = [x for x in arr[1:] if x >= pivot]
    return quicksort(lesser) + [pivot] + quicksort(greater)