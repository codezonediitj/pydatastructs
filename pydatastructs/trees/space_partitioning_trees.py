from pydatastructs.trees.binary_trees import Node
from collections import deque as Queue
from pydatastructs.linear_data_structures.arrays import _check_type

__all__ = [
    'OneDimensionalSegmentTree'
]

class OneDimensionalSegmentTree(object):
    """
    Represents one dimensional segment trees.

    Parameters
    ==========

    segs: list/tuple/set
        The segs should contains tuples/list/set of size 2
        denoting the start and end points of the intervals.

    Examples
    ========

    >>> from pydatastructs import OneDimensionalSegmentTree as ODST
    >>> segt = ODST([(3, 8), (9, 20)])
    >>> segt.build()
    >>> segt.tree[0].key
    [False, 2, 3, False]

    Note
    ====

    All the segments are assumed to be closed intervals,
    i.e., the ends are points of segments are also included in
    computation.

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Segment_tree

    """

    __slots__ = ['segments', 'tree', 'root_idx', 'cache']

    def __new__(cls, segs):
        obj = object.__new__(cls)
        if any((not isinstance(seg, (tuple, list, set)) or len(seg) != 2)
                for seg in segs):
                    raise ValueError('%s is invalid set of intervals'%(segs))
        for i in range(len(segs)):
            segs[i] = list(segs[i])
            segs[i].sort()
        obj.segments = [seg for seg in segs]
        obj.tree, obj.root_idx, obj.cache = [], None, False
        return obj

    def _union(self, i1, i2):
        """
        Helper function for taking union of two
        intervals.
        """
        return Node([i1.key[0], i1.key[1], i2.key[2], i2.key[3]], None)

    def _intersect(self, i1, i2):
        """
        Helper function for finding intersection of two
        intervals.
        """
        if i1 == None or i2 == None:
            return False
        if i2.key[1] < i1.key[2] or i1.key[1] < i2.key[2]:
            return True
        c1, c2 = False, False
        if i2.key[1] == i1.key[2]:
            c1 = i2.key[0] and i1.key[3]
        if i1.key[1] == i2.key[2]:
            c2 = i1.key[0] and i2.key[3]
        return c1 or c2

    def _contains(self, i1, i2):
        """
        Helper function for checking if the first interval
        is contained in second interval.
        """
        if i1 == None or i2 == None:
            return False
        if i1.key[1] < i2.key[1] and i1.key[2] > i2.key[2]:
            return True
        if i1.key[1] == i2.key[1] and i1.key[2] > i2.key[2]:
            return i1.key[0] and i2.key[0]
        if i1.key[1] < i2.key[1] and i1.key[2] == i2.key[2]:
            return i1.key[3] and i2.key[3]
        if i1.key[1] == i2.key[1] and i1.key[2] == i2.key[2]:
            return i1.key[3] and i2.key[3] and i1.key[0] and i2.key[0]

    def build(self):
        """
        Builds the segment tree from the segments,
        using iterative algorithm based on stacks.
        """
        if self.cache:
            return None
        endpoints = []
        for segment in self.segments:
            endpoints.extend(segment)
        endpoints.sort()

        elem_int = Queue()
        elem_int.append(Node([False, endpoints[0] - 1, endpoints[0], False], None))
        i = 0
        while i < len(endpoints) - 1:
            elem_int.append(Node([True, endpoints[i], endpoints[i], True], None))
            elem_int.append(Node([False, endpoints[i], endpoints[i+1], False], None))
            i += 1
        elem_int.append(Node([True, endpoints[i], endpoints[i], True], None))
        elem_int.append(Node([False, endpoints[i], endpoints[i] + 1, False], None))

        self.tree = []
        while len(elem_int) > 1:
            m = len(elem_int)
            while m >= 2:
                I1 = elem_int.popleft()
                I2 = elem_int.popleft()
                I = self._union(I1, I2)
                I.left = len(self.tree)
                I.right = len(self.tree) + 1
                self.tree.append(I1), self.tree.append(I2)
                elem_int.append(I)
                m -= 2
            if m & 1 == 1:
                Il = elem_int.popleft()
                elem_int.append(Il)

        Ir = elem_int.popleft()
        Ir.left, Ir.right = -3, -2
        self.tree.append(Ir)
        self.root_idx = -1

        for segment in self.segments:
            I = Node([True, segment[0], segment[1], True], None)
            calls = [self.root_idx]
            while calls:
                idx = calls.pop()
                if self._contains(I, self.tree[idx]):
                    if self.tree[idx].data == None:
                        self.tree[idx].data = []
                    self.tree[idx].data.append(I)
                    break
                if self.tree[idx].right == None:
                    rc = None
                else:
                    rc = self.tree[self.tree[idx].right]
                if self.tree[idx].left == None:
                    lc = None
                else:
                    lc = self.tree[self.tree[idx].left]
                if self._intersect(I, rc):
                    calls.append(self.tree[idx].right)
                if self._intersect(I, lc):
                    calls.append(self.tree[idx].left)
        self.cache = True

    def query(self, qx, init_node=None):
        pass


    def __str__(self):
        """
        Used for printing.
        """
        if not self.cache:
            self.build()
        str_tree = []
        for seg in self.tree:
            if seg.data == None:
                data = None
            else:
                data = [str(sd) for sd in seg.data]
            str_tree.append((seg.left, seg.key, data, seg.right))
        return str(str_tree)
