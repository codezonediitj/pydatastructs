from pydatastructs.utils.misc_util import (
    BinomialTreeNode, _check_type, Backend,
    raise_if_backend_is_not_python)

__all__ = [
    'BinomialTree'
]

class BinomialTree(object):
    """
    Represents binomial trees

    Parameters
    ==========

    root: BinomialTreeNode
        The root of the binomial tree.
        By default, None
    order: int
        The order of the binomial tree.
        By default, None
    backend: pydatastructs.Backend
        The backend to be used.
        Optional, by default, the best available
        backend is used.

    Examples
    ========

    >>> from pydatastructs import BinomialTree, BinomialTreeNode
    >>> root = BinomialTreeNode(1, 1)
    >>> tree = BinomialTree(root, 0)
    >>> tree.is_empty
    False

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Binomial_heap
    """
    __slots__ = ['root', 'order']

    def __new__(cls, root=None, order=None, **kwargs):
        raise_if_backend_is_not_python(
            cls, kwargs.get('backend', Backend.PYTHON))
        if root is not None and \
            not _check_type(root, BinomialTreeNode):
            raise TypeError("%s i.e., root should be of "
                             "type BinomialTreeNode."%(root))
        if order is not None and not _check_type(order, int):
            raise TypeError("%s i.e., order should be of "
                             "type int."%(order))
        obj = object.__new__(cls)
        if root is not None:
            root.is_root = True
        obj.root = root
        obj.order = order
        return obj

    @classmethod
    def methods(cls):
        return ['add_sub_tree', '__new__', 'is_empty']

    def add_sub_tree(self, other_tree):
        """
        Adds a sub tree to current tree.

        Parameters
        ==========

        other_tree: BinomialTree

        Raises
        ======

        ValueError: If order of the two trees
                    are different.
        """
        if not _check_type(other_tree, BinomialTree):
            raise TypeError("%s i.e., other_tree should be of "
                             "type BinomialTree"%(other_tree))
        if self.order != other_tree.order:
            raise ValueError("Orders of both the trees should be same.")
        self.root.children.append(other_tree.root)
        other_tree.root.parent = self.root
        other_tree.root.is_root = False
        self.order += 1

    @property
    def is_empty(self):
        return self.root is None
