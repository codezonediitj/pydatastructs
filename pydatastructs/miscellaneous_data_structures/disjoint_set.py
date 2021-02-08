from pydatastructs.utils import Set

__all__ = ['DisjointSetForest']


class DisjointSetForest(object):
    """
    Represents a forest of disjoint set trees.

    Examples
    ========

    >>> from pydatastructs import DisjointSetForest
    >>> dst = DisjointSetForest()
    >>> dst.make_set(1)
    >>> dst.make_set(2)
    >>> dst.union(1, 2)
    >>> dst.find_root(2).key
    1

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Disjoint-set_data_structure
    """

    __slots__ = ['tree']

    def __new__(cls):
        obj = object.__new__(cls)
        obj.tree = dict()
        return obj

    @classmethod
    def methods(cls):
        return ['make_set', '__new__', 'find_root', 'union']

    def make_set(self, key, data=None):
        """
        Adds a singleton set to the tree
        of disjoint sets with given key
        and optionally data.
        """
        if self.tree.get(key, None) is None:
            new_set = Set(key, data)
            self.tree[key] = new_set
            new_set.parent = new_set
            new_set.size = 1

    def find_root(self, key):
        """
        Finds the root of the set
        with the given key by path
        splitting algorithm.
        """
        if self.tree.get(key, None) is None:
            raise KeyError("Invalid key, %s" % key)
        _set = self.tree[key]
        while _set.parent is not _set:
            _set, _set.parent = _set.parent, _set.parent.parent
        return _set

    def union(self, key1, key2):
        """
        Takes the union of the two
        disjoint set trees with given
        keys. The union is done by size.
        """
        x_root = self.find_root(key1)
        y_root = self.find_root(key2)

        if x_root is not y_root:
            if x_root.size < y_root.size:
                x_root, y_root = y_root, x_root

            y_root.parent = x_root
            x_root.size += y_root.size
