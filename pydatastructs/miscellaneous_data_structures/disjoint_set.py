from pydatastructs.utils import Set

__all__ = ['DisjointSetTree']

class DisjointSetTree(object):

    __slots__ = ['tree']

    def __new__(cls):
        obj = object.__new__(cls)
        obj.tree = dict()
        return obj

    def make_set(self, key, data=None):
        if self.tree.get(key, None) is None:
            new_set = Set(key, data)
            self.tree[key] = new_set
            new_set.parent = new_set
            new_set.size = 1

    def find_root(self, key):
        if self.tree.get(key, None) is None:
            raise ValueError("Invalid key, %s"%(key))
        _set = self.tree[key]
        while _set.parent is not _set:
            _set, _set.parent = _set.parent, _set.parent.parent
        return _set

    def union(self, key1, key2):
        x_root = self.find_root(key1)
        y_root = self.find_root(key2)

        if x_root is y_root:
            return None

        if x_root.size < y_root.size:
            x_root, y_root = y_root, x_root

        y_root.parent = x_root
        x_root.size += y_root.size
