from pydatastructs.utils import TreeNode
from collections import deque as Queue
from pydatastructs.utils.misc_util import (
    _check_type, Backend,
    raise_if_backend_is_not_python)

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
    backend: pydatastructs.Backend
        The backend to be used.
        Optional, by default, the best available
        backend is used.

    Examples
    ========

    >>> from pydatastructs import OneDimensionalSegmentTree as ODST
    >>> segt = ODST([(3, 8), (9, 20)])
    >>> segt.build()
    >>> segt.tree[0].key
    [False, 2, 3, False]
    >>> len(segt.query(4))
    1

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

    def __new__(cls, segs, **kwargs):
        raise_if_backend_is_not_python(
            cls, kwargs.get('backend', Backend.PYTHON))
        obj = object.__new__(cls)
        if any((not isinstance(seg, (tuple, list, set)) or len(seg) != 2)
                for seg in segs):
                    raise ValueError('%s is invalid set of intervals'%(segs))
        for i in range(len(segs)):
            segs[i] = list(segs[i])
            segs[i].sort()
        obj.segments = list(segs)
        obj.tree, obj.root_idx, obj.cache = [], None, False
        return obj

    @classmethod
    def methods(cls):
        return ['build', 'query', '__str__']

    def _union(self, i1, i2):
        """
        Helper function for taking union of two
        intervals.
        """
        return TreeNode([i1.key[0], i1.key[1], i2.key[2], i2.key[3]], None)

    def _intersect(self, i1, i2):
        """
        Helper function for finding intersection of two
        intervals.
        """
        if i1 is None or i2 is None:
            return False
        if i1.key[2] < i2.key[1] or i2.key[2] < i1.key[1]:
            return False
        c1, c2 = None, None
        if i1.key[2] == i2.key[1]:
            c1 = (i1.key[3] and i2.key[0])
        if i2.key[2] == i1.key[1]:
            c2 = (i2.key[3] and i1.key[0])
        if c1 is False and c2 is False:
            return False
        return True

    def _contains(self, i1, i2):
        """
        Helper function for checking if the first interval
        is contained in second interval.
        """
        if i1 is None or i2 is None:
            return False
        if i1.key[1] < i2.key[1] and i1.key[2] > i2.key[2]:
            return True
        if i1.key[1] == i2.key[1] and i1.key[2] > i2.key[2]:
            return (i1.key[0] or not i2.key[0])
        if i1.key[1] < i2.key[1] and i1.key[2] == i2.key[2]:
            return i1.key[3] or not i2.key[3]
        if i1.key[1] == i2.key[1] and i1.key[2] == i2.key[2]:
            return not ((not i1.key[3] and i2.key[3]) or (not i1.key[0] and i2.key[0]))
        return False

    def _iterate(self, calls, I, idx):
        """
        Helper function for filling the calls
        stack. Used for imitating the stack based
        approach used in recursion.
        """
        if self.tree[idx].right is None:
            rc = None
        else:
            rc = self.tree[self.tree[idx].right]
        if self.tree[idx].left is None:
            lc = None
        else:
            lc = self.tree[self.tree[idx].left]
        if self._intersect(I, rc):
            calls.append(self.tree[idx].right)
        if self._intersect(I, lc):
            calls.append(self.tree[idx].left)
        return calls

    def build(self):
        """
        Builds the segment tree from the segments,
        using iterative algorithm based on queues.
        """
        if self.cache:
            return None
        endpoints = []
        for segment in self.segments:
            endpoints.extend(segment)
        endpoints.sort()

        elem_int = Queue()
        elem_int.append(TreeNode([False, endpoints[0] - 1, endpoints[0], False], None))
        i = 0
        while i < len(endpoints) - 1:
            elem_int.append(TreeNode([True, endpoints[i], endpoints[i], True], None))
            elem_int.append(TreeNode([False, endpoints[i], endpoints[i+1], False], None))
            i += 1
        elem_int.append(TreeNode([True, endpoints[i], endpoints[i], True], None))
        elem_int.append(TreeNode([False, endpoints[i], endpoints[i] + 1, False], None))

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
            I = TreeNode([True, segment[0], segment[1], True], None)
            calls = [self.root_idx]
            while calls:
                idx = calls.pop()
                if self._contains(I, self.tree[idx]):
                    if self.tree[idx].data is None:
                        self.tree[idx].data = []
                    self.tree[idx].data.append(I)
                    continue
                calls = self._iterate(calls, I, idx)
        self.cache = True

    def query(self, qx, init_node=None):
        """
        Queries the segment tree.

        Parameters
        ==========

        qx: int/float
            The query point

        init_node: int
            The index of the node from which the query process
            is to be started.

        Returns
        =======

        intervals: set
            The set of the intervals which contain the query
            point.

        References
        ==========

        .. [1] https://en.wikipedia.org/wiki/Segment_tree
        """
        if not self.cache:
            self.build()
        if init_node is None:
            init_node = self.root_idx
        qn = TreeNode([True, qx, qx, True], None)
        intervals = []
        calls = [init_node]
        while calls:
            idx = calls.pop()
            if _check_type(self.tree[idx].data, list):
                intervals.extend(self.tree[idx].data)
            calls = self._iterate(calls, qn, idx)
        return set(intervals)

    def __str__(self):
        """
        Used for printing.
        """
        if not self.cache:
            self.build()
        str_tree = []
        for seg in self.tree:
            if seg.data is None:
                data = None
            else:
                data = [str(sd) for sd in seg.data]
            str_tree.append((seg.left, seg.key, data, seg.right))
        return str(str_tree)
