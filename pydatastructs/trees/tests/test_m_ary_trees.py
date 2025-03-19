from pydatastructs.utils.misc_util import Backend
from pydatastructs.trees.m_ary_trees import MAryTree, FusionTree

def test_MAryTree():
    m = MAryTree(1, 1)
    assert str(m) == '[(1, 1)]'

def _test_FusionTree(backend):
    FT = FusionTree
    f_tree = FT(backend=backend)

    f_tree.insert(8, 8)
    f_tree.insert(3, 3)
    f_tree.insert(10, 10)
    f_tree.insert(1, 1)
    f_tree.insert(6, 6)
    f_tree.insert(4, 4)
    f_tree.insert(7, 7)
    f_tree.insert(14, 14)
    f_tree.insert(13, 13)

    assert f_tree.search(10) is not None
    assert f_tree.search(-1) is None

    assert f_tree.delete(13) is True
    assert f_tree.search(13) is None
    assert f_tree.delete(10) is True
    assert f_tree.search(10) is None
    assert f_tree.delete(3) is True
    assert f_tree.search(3) is None
    assert f_tree.delete(13) is False  # Already deleted

    expected_str = '[(8, 8), (1, 1), (6, 6), (4, 4), (7, 7), (14, 14)]'
    assert str(f_tree) == expected_str

    f_tree.insert(8, 9)
    assert f_tree.search(8) is not None

    large_key = 10**9
    f_tree.insert(large_key, large_key)
    assert f_tree.search(large_key) is not None

    expected_str = '[(8, 8), (1, 1), (6, 6), (4, 4), (7, 7), (14, 14), (8, 9), (1000000000, 1000000000)]'
    assert str(f_tree) == expected_str
    assert f_tree.delete(8) is True

    expected_str = '[(1, 1), (6, 6), (4, 4), (7, 7), (14, 14), (8, 9), (1000000000, 1000000000)]'
    assert str(f_tree) == expected_str

    FT = FusionTree
    f_tree = FT(8, 8, backend=backend)

    f_tree.insert(8, 8)
    f_tree.insert(3, 3)
    f_tree.insert(10, 10)
    f_tree.insert(1, 1)
    f_tree.insert(6, 6)
    f_tree.insert(4, 4)
    f_tree.insert(7, 7)
    f_tree.insert(14, 14)
    f_tree.insert(13, 13)

    assert f_tree.search(10) is not None
    assert f_tree.search(-1) is None

    assert f_tree.delete(13) is True
    assert f_tree.search(13) is None
    assert f_tree.delete(10) is True
    assert f_tree.search(10) is None
    assert f_tree.delete(3) is True
    assert f_tree.search(3) is None
    assert f_tree.delete(13) is False  # Already deleted

    expected_str = '[(8, 8), (8, 8), (1, 1), (6, 6), (4, 4), (7, 7), (14, 14)]'
    assert str(f_tree) == expected_str

    f_tree.insert(8, 9)
    assert f_tree.search(8) is not None

    large_key = 10**9
    f_tree.insert(large_key, large_key)
    assert f_tree.search(large_key) is not None

    expected_str = '[(8, 8), (8, 8), (1, 1), (6, 6), (4, 4), (7, 7), (14, 14), (8, 9), (1000000000, 1000000000)]'
    assert str(f_tree) == expected_str
    assert f_tree.delete(8) is True

    expected_str = '[(8, 8), (1, 1), (6, 6), (4, 4), (7, 7), (14, 14), (8, 9), (1000000000, 1000000000)]'
    assert str(f_tree) == expected_str


def test_FusionTree():
    _test_FusionTree(Backend.PYTHON)
