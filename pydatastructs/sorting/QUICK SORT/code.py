def quick_sort(arr, start, end):
    """
    Quick Sort algorithm: Sorts the array in ascending order.
    
    Parameters:
        arr (list): The list of elements to be sorted.
        start (int): The starting index of the array segment.
        end (int): The ending index of the array segment.
    """
    if start < end:
        # Partition the array and get the pivot index
        pivot_index = partition(arr, start, end)
        
        # Recursively sort the left subarray
        quick_sort(arr, start, pivot_index - 1)
        
        # Recursively sort the right subarray
        quick_sort(arr, pivot_index + 1, end)


def partition(arr, start, end):
    """
    Partitions the array around a pivot such that all elements smaller than
    or equal to the pivot are on the left, and all elements greater are on the right.
    
    Parameters:
        arr (list): The list of elements to be partitioned.
        start (int): The starting index of the array segment.
        end (int): The ending index of the array segment (pivot).
    
    Returns:
        int: The index of the pivot element after partitioning.
    """
    pivot = arr[end]  # Choose the last element as the pivot
    partition_index = start  # Initialize the partition index

    for i in range(start, end):
        if arr[i] <= pivot:
            # Swap if the current element is smaller than or equal to the pivot
            arr[i], arr[partition_index] = arr[partition_index], arr[i]
            partition_index += 1

    # Place the pivot element at the correct position
    arr[partition_index], arr[end] = arr[end], arr[partition_index]
    return partition_index


# Example Usage
if __name__ == "__main__":
    # Input array
    array = [8, 3, 1, 7, 0, 10, 2]
    print("Original Array:", array)

    # Perform Quick Sort
    quick_sort(array, 0, len(array) - 1)
    
    # Output sorted array
    print("Sorted Array:", array)
