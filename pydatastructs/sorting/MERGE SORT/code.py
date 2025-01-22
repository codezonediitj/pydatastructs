def merge_sort(arr):
    """
    Function to perform Merge Sort on a given list.

    Args:
    arr (list): Unsorted list to be sorted.

    Returns:
    list: Sorted list in ascending order.
    """
    if len(arr) > 1:
        # Finding the middle of the array to divide it
        mid = len(arr) // 2
        
        # Dividing the array into two halves
        left_half = arr[:mid]
        right_half = arr[mid:]

        # Recursively sorting both halves
        merge_sort(left_half)
        merge_sort(right_half)

        # Initializing pointers for left, right, and the merged array
        i = j = k = 0

        # Merging the two sorted halves into a single sorted array
        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1

        # Checking if any element remains in left_half
        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1

        # Checking if any element remains in right_half
        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1

    return arr

# Example usage:
if __name__ == "__main__":
    example_arr = [38, 27, 43, 3, 9, 82, 10]
    print("Original Array:", example_arr)
    sorted_arr = merge_sort(example_arr)
    print("Sorted Array:", sorted_arr)
