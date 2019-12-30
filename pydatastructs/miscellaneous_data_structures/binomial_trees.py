from pydatastructs.utils.misc_util import BinomialTreeNode, _check_type

__all__ = [
    'BinomialTree'
]

class BinomialTree(object):
    """
    """
    __slots__ = ['root', 'order']

    def __new__(cls, root=None, order=None):
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

    def add_sub_tree(self, other_tree):
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
