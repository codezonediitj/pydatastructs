__all__ = ['FenwickTree']
class FenwickTree():
    def __init__(self, array):
        self.size = len(array) + 1
        self.tree = [0] * (self.size + 1)
        self.array = array
        self.flag = [0] * (self.size-1)
        for index in range(self.size-1):
            self.update(index, array[index])
    def update(self, index, value):
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
        index += 1
        sum = 0
        while(index > 0):
            sum += self.tree[index]
            index = index - (index & (-index))
        return sum
    def get_sum(self, left_index, right_index):
        if(left_index >= 1):
            return self.get_prefix_sum(right_index) - self.get_prefix_sum(left_index - 1)
        else:
            return self.get_prefix_sum(right_index)
