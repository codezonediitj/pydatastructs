from .stack import Stack
from pydatastructs.utils.misc_util import (TreeNode,
    Backend, raise_if_backend_is_not_python)

__all__ = ['ArraySegmentTree']

class ArraySegmentTree(object):
    """
    Represents the segment tree data structure,
    defined on arrays.

    Parameters
    ==========

    array: Array
        The array to be used for filling the segment tree.
    func: callable
        The function to be used for filling the segment tree.
        It should accept only one tuple as an argument. The
        size of the tuple will be either 1 or 2 and any one
        of the elements can be `None`. You can treat `None` in
        whatever way you want. For example, in case of minimum
        values, `None` can be treated as infinity. We provide
        the following which can be used as an argument value for this
        parameter,

        `minimum` - For range minimum queries.

        `greatest_common_divisor` - For queries finding greatest
                                    common divisor of a range.

        `summation` - For range sum queries.
    dimensions: int
        The number of dimensions of the array to be used
        for the segment tree.
        Optional, by default 1.
    backend: pydatastructs.Backend
        The backend to be used.
        Optional, by default, the best available
        backend is used.

    Examples
    ========

    >>> from pydatastructs import ArraySegmentTree, minimum
    >>> from pydatastructs import OneDimensionalArray
    >>> arr = OneDimensionalArray(int, [1, 2, 3, 4, 5])
    >>> s_t = ArraySegmentTree(arr, minimum)
    >>> s_t.build()
    >>> s_t.query(0, 1)
    1
    >>> s_t.query(1, 3)
    2
    >>> s_t.update(2, -1)
    >>> s_t.query(1, 3)
    -1
    >>> arr = OneDimensionalArray(int, [1, 2])
    >>> s_t = ArraySegmentTree(arr, minimum)
    >>> s_t.build()
    >>> str(s_t)
    "['((0, 1), 1)', '((0, 0), 1)', '', '', '((1, 1), 2)', '', '']"

    References
    ==========

    .. [1] https://cp-algorithms.com/data_structures/segment_tree.html
    """
    def __new__(cls, array, func, **kwargs):

        dimensions = kwargs.pop("dimensions", 1)
        if dimensions == 1:
            return OneDimensionalArraySegmentTree(array, func, **kwargs)
        else:
            raise NotImplementedError("ArraySegmentTree do not support "
                                      "{}-dimensional arrays as of now.".format(dimensions))

    def build(self):
        """
        Generates segment tree nodes when called.
        Nothing happens if nodes are already generated.
        """
        raise NotImplementedError(
            "This is an abstract method.")

    def update(self, index, value):
        """
        Updates the value at given index.
        """
        raise NotImplementedError(
            "This is an abstract method.")

    def query(self, start, end):
        """
        Queries [start, end] range according
        to the function provided while constructing
        `ArraySegmentTree` object.
        """
        raise NotImplementedError(
            "This is an abstract method.")

    def __str__(self):
        recursion_stack = Stack(implementation='linked_list')
        recursion_stack.push(self._root)
        to_be_printed = []
        while not recursion_stack.is_empty:
            node = recursion_stack.pop().key
            if node is not None:
                to_be_printed.append(str((node.key, node.data)))
            else:
                to_be_printed.append('')
            if node is not None:
                recursion_stack.push(node.right)
                recursion_stack.push(node.left)
        return str(to_be_printed)


class OneDimensionalArraySegmentTree(ArraySegmentTree):

    __slots__ = ["_func", "_array", "_root", "_backend"]

    def __new__(cls, array, func, **kwargs):
        backend = kwargs.get('backend', Backend.PYTHON)
        raise_if_backend_is_not_python(cls, backend)

        obj = object.__new__(cls)
        obj._func = func
        obj._array = array
        obj._root = None
        obj._backend = backend
        return obj

    @classmethod
    def methods(self):
        return ['__new__', 'build', 'update',
                'query']

    @property
    def is_ready(self):
        return self._root is not None

    def build(self):
        if self.is_ready:
            return

        recursion_stack = Stack(implementation='linked_list')
        node = TreeNode((0, len(self._array) - 1), None, backend=self._backend)
        node.is_root = True
        self._root = node
        recursion_stack.push(node)

        while not recursion_stack.is_empty:
            node = recursion_stack.peek.key
            start, end = node.key
            if start == end:
                node.data = self._array[start]
                recursion_stack.pop()
                continue

            if (node.left is not None and
                node.right is not None):
                recursion_stack.pop()
                node.data = self._func((node.left.data, node.right.data))
            else:
                mid = (start + end) // 2
                if node.left is None:
                    left_node = TreeNode((start, mid), None)
                    node.left = left_node
                    recursion_stack.push(left_node)
                if node.right is None:
                    right_node = TreeNode((mid + 1, end), None)
                    node.right = right_node
                    recursion_stack.push(right_node)

    def update(self, index, value):
        if not self.is_ready:
            raise ValueError("{} tree is not built yet. ".format(self) +
                             "Call .build method to prepare the segment tree.")

        recursion_stack = Stack(implementation='linked_list')
        recursion_stack.push((self._root, None))

        while not recursion_stack.is_empty:
            node, child = recursion_stack.peek.key
            start, end = node.key
            if start == end:
                self._array[index] = value
                node.data = value
                recursion_stack.pop()
                if not recursion_stack.is_empty:
                    parent_node = recursion_stack.pop()
                    recursion_stack.push((parent_node.key[0], node))
                continue

            if child is not None:
                node.data = self._func((node.left.data, node.right.data))
                recursion_stack.pop()
                if not recursion_stack.is_empty:
                    parent_node = recursion_stack.pop()
                    recursion_stack.push((parent_node.key[0], node))
            else:
                mid = (start + end) // 2
                if start <= index and index <= mid:
                    recursion_stack.push((node.left, None))
                else:
                    recursion_stack.push((node.right, None))

    def _query(self, node, start, end, l, r):
        if r < start or end < l:
            return None

        if l <= start and end <= r:
            return node.data

        mid = (start + end) // 2
        left_result = self._query(node.left, start, mid, l, r)
        right_result = self._query(node.right, mid + 1, end, l, r)
        return self._func((left_result, right_result))

    def query(self, start, end):
        if not self.is_ready:
            raise ValueError("{} tree is not built yet. ".format(self) +
                             "Call .build method to prepare the segment tree.")

        return self._query(self._root, 0, len(self._array) - 1,
                           start, end)
