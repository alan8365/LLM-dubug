def find_in_sorted(arr, x):
    def binsearch(start, end):
        if start >= end:
            return -1
        mid = start + (end - start) // 2
        if x < arr[mid]:
            return binsearch(start, mid)
        elif x > arr[mid]:
            return binsearch(mid + 1, end)
        else:
            return mid

    return binsearch(0, len(arr))
The fixed code includes the following changes:
- In the binsearch function, the condition `if start == end` has been changed to `if start >= end`. This ensures that the function will return -1 if the search range is empty or if the element is not found.
- In the binsearch function, the recursive call in the `elif x > arr[mid]` branch has been changed to `return binsearch(mid + 1, end)`. This ensures that the next search range starts from the next element after the middle element, avoiding potential infinite recursion.
- The fixed code now correctly handles the case when the element is not found and returns -1.