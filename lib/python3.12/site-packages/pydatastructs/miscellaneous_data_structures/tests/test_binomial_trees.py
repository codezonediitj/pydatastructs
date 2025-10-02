from pydatastructs.miscellaneous_data_structures.binomial_trees import BinomialTree
from pydatastructs.utils.raises_util import raises
from pydatastructs.utils.misc_util import BinomialTreeNode

# only tests the corner cases
def test_BinomialTree():
    assert raises(TypeError, lambda: BinomialTree(1, 1))
    assert raises(TypeError, lambda: BinomialTree(None, 1.5))

    bt = BinomialTree()
    assert raises(TypeError, lambda: bt.add_sub_tree(None))
    bt1 = BinomialTree(BinomialTreeNode(1, 1), 0)
    node = BinomialTreeNode(2, 2)
    node.add_children(BinomialTreeNode(3, 3))
    bt2 = BinomialTree(node, 1)
    assert raises(ValueError, lambda: bt1.add_sub_tree(bt2))
    assert bt1.is_empty is False
