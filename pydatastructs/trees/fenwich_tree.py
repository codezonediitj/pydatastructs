class fenwich_tree:
    """
    Implementation of Fenwich tree/Binary Indexed Tree
    """

    def __init__(self, size_or_array):
        """
        Initializes the Fenwich Tree.

        Args:
            size_or_array: size of array the tree will represent or array of values
        """

        if isinstance(size_or_array, int):
            self.size = size_or_array
            self.tree = [0] * (self.size + 1)
            self.original_array = [0] * self.size 
        elif isinstance(size_or_array, list):
            self.original_array = list(size_or_array)
            self.size = len(self.original_array)
            self.tree = [0] * (self.size + 1)
            for i, val in enumerate(self.original_array):
                self._update_tree(i, val)
        else:
            raise ValueError("size_or_array must be an integer or a list.")
        
    def _update_tree(self, index, delta):
        """
        Internal helper to update the Fenwick Tree after a change in the original array.
        """
        index += 1  # Fenwick Tree is 1-indexed
        while index <= self.size:
            self.tree[index] += delta
            index += index & (-index)

    def update(self, index, value):
        """
        Updates the value at the given index in the original array and the Fenwick Tree.

        Args:
            index: The index to update (0-based).
            value: The new value.
        """
        if not (0 <= index < self.size):
            raise IndexError("Index out of bounds")
        delta = value - self.original_array[index]
        self.original_array[index] = value
        self._update_tree(index, delta)

    def prefix_sum(self, index):
        """
        Calculates the prefix sum up to the given index (inclusive).

        Args:
            index: The index up to which to calculate the sum (0-based).

        Returns:
            The prefix sum.
        """
        if not (0 <= index < self.size):
            raise IndexError("Index out of bounds")
        index += 1  #
        sum_val = 0
        while index > 0:
            sum_val += self.tree[index]
            index -= index & (-index)  
        return sum_val
    
    def range_sum(self, start_index, end_index):
        """
        Calculates the sum of elements within the given range (inclusive).

        Args:
            start_index: The starting index of the range (0-based).
            end_index: The ending index of the range (0-based).

        Returns:
            The sum of elements in the range.
        """
        if not (0 <= start_index <= end_index < self.size):
            raise IndexError("Indices out of bounds")
        if start_index == 0:
            return self.prefix_sum(end_index)
        else:
            return self.prefix_sum(end_index) - self.prefix_sum(start_index - 1)