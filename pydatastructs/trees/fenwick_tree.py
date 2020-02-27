__all__ = ['FenwickTree']

class FenwickTree():
    def __new__(cls, array):
        obj = super(FenwickTree, cls).__new__(cls)
        obj.size = len(array) + 1
        obj.tree = [0] * (obj.size + 1)
        obj.array = array
        obj.flag = [0] * (obj.size-1)
        for index in range(obj.size-1):
            obj.update(index, array[index])
        return obj

    def update(self, index, value):
        """
        Update sum in Fenwick tree.

        Parameters
        ==========

        index
            Index of element to be updated.
        value
            The value to be inserted.

        Returns
        =======

        None
        """
        if(self.flag[index] == 0):
            self.flag[index] = 1
            index += 1
            while(index < self.size):
                self.tree[index] += value
                index = index + (index & (-index))
        else:
            value = value - self.array[index]
            index += 1
            while(index < self.size):
                self.tree[index] += value
                index = index + (index & (-index))

    def get_prefix_sum(self, index):
        """
        Get sum of elements from index 0 to given index.

        Parameters
        ==========

        index
            Index till which sum has to be calculated.
        Returns
        =======

        int
        """
        index += 1
        sum = 0
        while(index > 0):
            sum += self.tree[index]
            index = index - (index & (-index))
        return sum

    def get_sum(self, left_index, right_index):
        """
        Get sum of elements from left_index to right_index.

        Parameters
        ==========

        left_index
            Starting index from where sum has to be computed.
        right_index
            Ending index till where sum has to be computed.

        Returns
        =======

        int
        """
        if(left_index >= 1):
            return self.get_prefix_sum(right_index) - self.get_prefix_sum(left_index - 1)
        else:
            return self.get_prefix_sum(right_index)
