import random
from segment_tree import SegmentTree


def gen_range(list_size):
    """
    Generates range [L, R] for querying.
    
    """
    
    left = random.randint(0, list_size - 1)
    right = random.randint(left, list_size - 1)

    return left, right


def random_test():
    """
    Random test for the Segment Tree using random list
    of values, random range queries.
     
    """
    
    random_list = [random.randint(-10 ** 6, 10 ** 6) for _ in range(10 ** 5)]
    t = SegmentTree(random_list)

    for _ in range(random.randint(10 ** 3, 10 ** 6)):

        l, r = gen_range(len(random_list))

        query_type = random.randint(1, 3)

        if query_type == 1:

            print(t.query(1, 0, t.get_list_len() - 1, l, r))

        elif query_type == 2:

            pos = random.randint(0, len(random_list) - 1)
            new_val = random.randint(-10 ** 6, 10 ** 6)

            t.point_update(pos, new_val)

        else:

            add_val = random.randint(-10 ** 6, 10 ** 6)
            t.range_update(1, 0, t.get_list_len() - 1, l, r, add_val)


def static_test():
    """
    Static test with known changes during updates
    and queries of the tree with appropriate assertions.
    
    """
    
    static_list = [3, 6, 9, 10, 4]
    t = SegmentTree(static_list)

    assert t.tree_size == 16

    print(t.tree)
    print(t.lazy)

    assert t.query(1, 0, t.get_list_len() - 1, 1, 3) == 25

    t.point_update(4, 17)
    assert t.query(1, 0, t.get_list_len() - 1, 0, 2) == 18
    assert t.query(1, 0, t.get_list_len() - 1, 1, 4) == 42

    t.range_update(1, 0, t.get_list_len() - 1, 0, 4, -29)
    t.range_update(1, 0, t.get_list_len() - 1, 2, 3, 10)
    assert t.query(1, 0, t.get_list_len() - 1, 1, 4) == -54

    t.point_update(0, 0)
    t.point_update(1, 9)
    t.point_update(2, 2)
    t.point_update(3, 1)
    t.point_update(4, 0)

    assert t.query(1, 0, t.get_list_len() - 1, 0, 4) == 12
    assert t.lazy.count(0) == 14


# random_test()

static_test()
