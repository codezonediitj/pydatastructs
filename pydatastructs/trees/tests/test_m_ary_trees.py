from pydatastructs.utils.misc_util import Backend
from pydatastructs.trees.m_ary_trees import MAryTree, ParentPointerTree


def test_MAryTree():
    m = MAryTree(1, 1)
    assert str(m) == '[(1, 1)]'


def _test_ParentPointerTree(backend):
    PPT = ParentPointerTree

    tree = PPT(1, "root", backend=backend)
    assert tree.root_idx == 0
    assert tree.tree[0].key == 1
    assert tree.tree[0].data == "root"
    assert tree.tree[0].parent is None

    tree.insert(1, 2, "child_1")
    tree.insert(1, 3, "child_2")
    tree.insert(1, 4, "child_3")
    assert tree.size == 4
    assert tree.tree[1].key == 2
    assert tree.tree[1].data == "child_1"
    assert tree.tree[1].parent == tree.tree[0]
    assert tree.tree[2].key == 3
    assert tree.tree[2].data == "child_2"
    assert tree.tree[2].parent == tree.tree[0]
    assert tree.tree[3].key == 4
    assert tree.tree[3].data == "child_3"
    assert tree.tree[3].parent == tree.tree[0]

    assert tree.search(2).data == "child_1"
    assert tree.search(3).data == "child_2"
    assert tree.search(4).data == "child_3"
    assert tree.search(5) is None
    assert tree.search(2, parent=True) == tree.tree[0]

    tree.insert(2, 5, "child_4")
    tree.insert(2, 6, "child_5")
    assert tree.least_common_ancestor(5, 6) == tree.tree[1]
    assert tree.least_common_ancestor(5, 3) == tree.tree[0]
    assert tree.least_common_ancestor(2, 4) == tree.tree[0]
    assert tree.least_common_ancestor(5, 7) is None

    assert tree.delete(5) is True
    assert tree.search(5) is None
    assert tree.size == 5
    assert tree.delete(6) is True
    assert tree.search(6) is None
    assert tree.size == 4
    assert tree.delete(10) is None

    expected = '''[(1, 'root', 'None'), (2, 'child_1', "(1, 'root')"), (3, 'child_2', "(1, 'root')"), (4, 'child_3', "(1, 'root')")]'''
    assert str(tree) == expected

    empty_tree = PPT(backend=backend)
    assert empty_tree.size == 0
    assert empty_tree.search(1) is None
    assert empty_tree.delete(1) is None
    assert empty_tree.least_common_ancestor(1, 2) is None

    empty_tree.insert(None, 7, "child_6")

    expected = '''[(7, 'child_6', 'None')]'''
    assert str(empty_tree) == expected

def test_ParentPointerTree():
    _test_ParentPointerTree(Backend.PYTHON)
