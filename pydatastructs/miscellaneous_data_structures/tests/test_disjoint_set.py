from pydatastructs import DisjointSetForest
from pydatastructs.utils.raises_util import raises


def test_DisjointSetForest():
    dst = DisjointSetForest()
    for i in range(8):
        dst.make_set(i + 1)

    dst.union(1, 2)
    dst.union(1, 5)
    dst.union(1, 6)
    dst.union(1, 8)
    dst.union(3, 4)

    assert (dst.find_root(1) == dst.find_root(2) == dst.find_root(5) == dst.find_root(6) == dst.find_root(8))
    assert dst.find_root(3) == dst.find_root(4)
    assert dst.find_root(7).key == 7

    assert raises(KeyError, lambda: dst.find_root(9))
    dst.union(3, 1)
    assert dst.find_root(3).key == 1
