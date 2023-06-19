__all__ = [
    'Multiset'
]


class Multiset:
    def __init__(self, *args):
        # TODO: Implement dict in pydatastructs
        self.counter = dict()
        from pydatastructs.trees import RedBlackTree
        self.tree = RedBlackTree()
        self._n = 0
        for arg in args:
            self.add(arg)

    def add(self, element):
        self.counter[element]  = self.counter.get(element, 0) + 1
        self._n += 1
        if self.counter[element] == 1:
            self.tree.insert(element)

    def remove(self, element):
        if self.counter[element] == 1:
            self.tree.delete(element)
        if self.counter.get(element, 0) > 0:
            self._n -= 1
            self.counter[element] -= 1

    def lower_bound(self, element):
        return self.tree.lower_bound(element)

    def upper_bound(self, element):
        return self.tree.upper_bound(element)

    def __contains__(self, element):
        return self.counter.get(element, 0) > 0

    def __len__(self):
        return self._n

    def count(self, element):
        return self.counter.get(element, 0)
