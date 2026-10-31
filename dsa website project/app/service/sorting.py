"""Merge sort implementation used to order expenses for the DSA project."""


def merge_sort(items, key, descending=False):
    """Return a sorted copy using merge sort (O(n log n))."""
    if len(items) < 2:
        return list(items)
    middle = len(items) // 2
    left = merge_sort(items[:middle], key, descending)
    right = merge_sort(items[middle:], key, descending)
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        left_value, right_value = key(left[i]), key(right[j])
        take_left = left_value >= right_value if descending else left_value <= right_value
        if take_left:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    return result + left[i:] + right[j:]
