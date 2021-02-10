from pydatastructs.utils.raises_util import raises
from pydatastructs.trees.btree import BTree
from pydatastructs.utils import BNode

def test_BTree():

    tree = BTree()
    f, t = False, True

    tree.insert(1)
    tree.insert(2)
    tree.insert(5)
    assert str(tree._path_to(5)) == '[(<Branch 2>, 1), (<Leaf 5>, 0)]'
    assert tree.__contains__(4) == f
    assert tree.__contains__(1) == t
    assert list(iter(tree)) == [1, 2, 5]
    #assert tree._present(5,[(tree.LEAF, 1)])

    raises(ValueError, lambda: tree.remove(4))
    assert str(repr(tree)) == '<Branch 2>  <Leaf 1>  <Leaf 5>'

    tree.insert(6)
    tree.insert(9)

    bt = BTree(10)

    l = range(20)
    for i, item in enumerate(l):
        bt.insert(item)
        assert list(bt) == list(l[:i + 1])

    tr = BTree(3)

    for a in range(10):
        tr.insert(a)
    assert repr(tr) == '<Branch 3, 6>  <Leaf 0, 1, 2>  <Leaf 4, 5>  <Leaf 7, 8, 9>'
    assert list(tr) == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    for a in range(2,10,2):
        tr.remove(a)
    assert str(tr._path_to(9)) == '[(<Branch 3, 7>, 2), (<Leaf 9>, 0)]'
    assert list(tr) == [0, 1, 3, 5, 7, 9]
    assert repr(tr) == '<Branch 3, 7>  <Leaf 0, 1>  <Leaf 5>  <Leaf 9>'

    tree = BTree(5)

    tree.insert('H')
    tree.insert('E')
    assert repr(tree) == '<Leaf E, H>'
    tree.remove('H')
    assert raises(ValueError, lambda: tree.remove('I'))

    bt = BTree.bulkload(range(50), 20)
    assert list(bt) == list(range(50))

def test_BNode():
    node = BNode(BTree, [3, 4], [6, 7, 9])
    assert repr(node) == '<Branch 3, 4>'
    node.split()
    assert repr(node) == '<Branch 3>'
