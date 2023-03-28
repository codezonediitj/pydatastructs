from pydatastructs.utils import Set
from pydatastructs.utils.misc_util import (
    Backend, raise_if_backend_is_not_python)

__all__ = ['DisjointSetForest']

class DisjointSetForest(object):
    """
    Represents a forest of disjoint set trees.

    Parameters
    ==========

    backend: pydatastructs.Backend
        The backend to be used.
        Optional, by default, the best available
        backend is used.

    Examples
    ========

    >>> from pydatastructs import DisjointSetForest
    >>> dst = DisjointSetForest()
    >>> dst.make_set(1)
    >>> dst.make_set(2)
    >>> dst.union(1, 2)
    >>> dst.find_root(2).key
    1
    >>> dst.make_root(2)
    >>> dst.find_root(2).key
    2

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Disjoint-set_data_structure
    """

    __slots__ = ['tree']

    def __new__(cls, **kwargs):
        raise_if_backend_is_not_python(
            cls, kwargs.get('backend', Backend.PYTHON))
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
            raise KeyError("Invalid key, %s"%(key))
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

    def make_root(self, key):
        """
        Finds the set to which the key belongs
        and makes it as the root of the set.
        """
        if self.tree.get(key, None) is None:
            raise KeyError("Invalid key, %s"%(key))

        key_set = self.tree[key]
        if key_set.parent is not key_set:
            current_parent = key_set.parent
            # Remove this key subtree size from all its ancestors
            while current_parent.parent is not current_parent:
                current_parent.size -= key_set.size
                current_parent = current_parent.parent

            all_set_size = current_parent.size # This is the root node
            current_parent.size -= key_set.size

            # Make parent of current root as key
            current_parent.parent = key_set
            # size of new root will be same as previous root's size
            key_set.size = all_set_size
            # Make parent of key as itself
            key_set.parent = key_set

    def find_size(self, key):
        """
        Finds the size of set to which the key belongs.
        """
        if self.tree.get(key, None) is None:
            raise KeyError("Invalid key, %s"%(key))

        return self.find_root(key).size

    def disjoint_sets(self):
        """
        Returns a list of disjoint sets in the data structure.
        """
        result = dict()
        for key in self.tree.keys():
            parent = self.find_root(key).key
            members = result.get(parent, [])
            members.append(key)
            result[parent] = members
        sorted_groups = []
        for v in result.values():
            sorted_groups.append(v)
            sorted_groups[-1].sort()
        sorted_groups.sort()
        return sorted_groups
