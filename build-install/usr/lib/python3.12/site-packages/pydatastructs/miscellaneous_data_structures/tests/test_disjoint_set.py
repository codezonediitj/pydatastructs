from pydatastructs import DisjointSetForest
from pydatastructs.utils.raises_util import raises

def test_DisjointSetForest():

    dst = DisjointSetForest()
    for i in range(8):
        dst.make_set(i+1)

    dst.union(1, 2)
    dst.union(1, 5)
    assert dst.find_size(2) == 3
    dst.union(1, 6)
    dst.union(1, 8)
    dst.union(3, 4)
    assert dst.find_size(3) == 2

    assert (dst.find_root(1) == dst.find_root(2) ==
            dst.find_root(5) == dst.find_root(6) == dst.find_root(8))
    assert dst.disjoint_sets() == [[1, 2, 5, 6, 8], [3, 4], [7]]
    assert dst.find_root(3) == dst.find_root(4)
    assert dst.find_root(7).key == 7

    assert raises(KeyError, lambda: dst.find_root(9))
    assert raises(KeyError, lambda: dst.find_size(9))
    dst.union(3, 1)
    assert dst.find_root(3).key == 1
    assert dst.find_root(5).key == 1
    dst.make_root(6)
    assert dst.disjoint_sets() == [[1, 2, 3, 4, 5, 6, 8], [7]]
    assert dst.find_root(3).key == 6
    assert dst.find_root(5).key == 6
    dst.make_root(5)
    assert dst.find_root(1).key == 5
    assert dst.find_root(5).key == 5
    assert raises(KeyError, lambda: dst.make_root(9))

    dst = DisjointSetForest()
    for i in range(6):
        dst.make_set(i)
    assert dst.tree[2].size == 1
    dst.union(2, 3)
    assert dst.tree[2].size == 2
    assert dst.tree[3].size == 1
    dst.union(1, 4)
    dst.union(2, 4)
    assert dst.disjoint_sets() == [[0], [1, 2, 3, 4], [5]]
    # current tree
    ###############
    #       2
    #      / \
    #     1   3
    #    /
    #   4
    ###############
    assert dst.tree[2].size == 4
    assert dst.tree[1].size == 2
    assert dst.tree[3].size == dst.tree[4].size == 1
    dst.make_root(4)
    # New tree
    ###############
    #       4
    #       |
    #       2
    #      / \
    #     1   3
    ###############
    assert dst.tree[4].size == 4
    assert dst.tree[2].size == 3
    assert dst.tree[1].size == dst.tree[3].size == 1
