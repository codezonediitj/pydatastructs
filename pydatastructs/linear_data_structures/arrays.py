from pydatastructs.utils.misc_util import (
    _check_type, NoneType, Backend,
    raise_if_backend_is_not_python)
from pydatastructs.linear_data_structures._backend.cpp import _arrays

__all__ = [
    'OneDimensionalArray',
    'MultiDimensionalArray',
    'DynamicOneDimensionalArray'
]

class Array(object):
    """
    Abstract class for arrays in pydatastructs.
    """
    def __str__(self) -> str:
        return str(self._data)

class OneDimensionalArray(Array):
    """
    Represents one dimensional static arrays of
    fixed size.

    Parameters
    ==========

    dtype: type
        A valid object type.
    size: int
        The number of elements in the array.
    elements: list
        The elements in the array, all should
        be of same type.
    init: a python type
        The initial value with which the element has
        to be initialized. By default none, used only
        when the data is not given.
    backend: pydatastructs.Backend
        The backend to be used.
        Optional, by default, the best available
        backend is used.

    Raises
    ======

    ValueError
        When the number of elements in the list do not
        match with the size.
        More than three parameters are passed as arguments.
        Types of arguments is not as mentioned in the docstring.

    Note
    ====

    At least one parameter should be passed as an argument along
    with the dtype.

    Examples
    ========

    >>> from pydatastructs import OneDimensionalArray
    >>> arr = OneDimensionalArray(int, 5)
    >>> arr.fill(6)
    >>> arr[0]
    6
    >>> arr[0] = 7.2
    >>> arr[0]
    7

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Array_data_structure#One-dimensional_arrays
    """

    __slots__ = ['_size', '_data', '_dtype']

    def __new__(cls, dtype=NoneType, *args, **kwargs):
        backend = kwargs.get('backend', Backend.PYTHON)
        if backend == Backend.CPP:
            return _arrays.OneDimensionalArray(dtype, *args, **kwargs)
        if dtype is NoneType:
            raise ValueError("Data type is not defined.")
        if len(args) not in (1, 2):
            raise ValueError("Too few arguments to create a 1D array,"
                                " pass either size of the array"
                                " or list of elements or both.")
        obj = Array.__new__(cls)
        obj._dtype = dtype
        if len(args) == 2:
            if _check_type(args[0], list) and \
                _check_type(args[1], int):
                for i in range(len(args[0])):
                    if _check_type(args[0][i], dtype) is False:
                        args[0][i] = dtype(args[0][i])
                size, data = args[1], list(args[0])
            elif _check_type(args[1], list) and \
                _check_type(args[0], int):
                for i in range(len(args[1])):
                    if _check_type(args[1][i], dtype) is False:
                        args[1][i] = dtype(args[1][i])
                size, data = args[0], list(args[1])
            else:
                raise TypeError("Expected type of size is int and "
                                "expected type of data is list/tuple.")
            if size != len(data):
                raise ValueError("Conflict in the size, %s and length of data, %s"
                                 %(size, len(data)))
            obj._size, obj._data = size, data

        elif len(args) == 1:
            if _check_type(args[0], int):
                obj._size = args[0]
                init = kwargs.get('init', None)
                obj._data = [init for i in range(args[0])]
            elif _check_type(args[0], (list, tuple)):
                for i in range(len(args[0])):
                    if _check_type(args[0][i], dtype) is False:
                        args[0][i] = dtype(args[0][i])
                obj._size, obj._data = len(args[0]), \
                                        list(args[0])
            else:
                raise TypeError("Expected type of size is int and "
                                "expected type of data is list/tuple.")

        return obj

    @classmethod
    def methods(cls):
        return ['__new__', '__getitem__',
        '__setitem__', 'fill', '__len__']

    def __getitem__(self, i):
        if i >= self._size or i < 0:
            raise IndexError(("Index, {} out of range, "
                              "[{}, {}).".format(i, 0, self._size)))
        return self._data.__getitem__(i)

    def __setitem__(self, idx, elem):
        if elem is None:
            self._data[idx] = None
        else:
            if _check_type(elem, self._dtype) is False:
                elem = self._dtype(elem)
            self._data[idx] = elem

    def fill(self, elem):
        elem = self._dtype(elem)
        for i in range(self._size):
            self._data[i] = elem

    def __len__(self):
        return self._size

class MultiDimensionalArray(Array):
    """
    Represents a multi-dimensional array.

    Parameters
    ==========

    dtype: type
        A valid object type.
    *args: int
        The dimensions of the array.
    backend: pydatastructs.Backend
        The backend to be used.
        Optional, by default, the best available
        backend is used.

    Raises
    ======

    IndexError
        Index goes out of boundaries, or
        the number of index given is not
        the same as the number of dimensions.
    ValueError
        When there's no dimensions or the
        dimension size is 0.

    Examples
    ========

    >>> from pydatastructs import MultiDimensionalArray as MDA
    >>> arr = MDA(int, 5, 6, 9)
    >>> arr.fill(32)
    >>> arr[3, 0, 0]
    32
    >>> arr[3, 0, 0] = 7
    >>> arr[3, 0, 0]
    7

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Array_data_structure#Multidimensional_arrays

    """
    __slots__ = ['_sizes', '_data', '_dtype']

    def __new__(cls, dtype: type = NoneType, *args, **kwargs):
        raise_if_backend_is_not_python(
            cls, kwargs.get('backend', Backend.PYTHON))
        if dtype is NoneType:
            raise ValueError("Data type is not defined.")
        elif not args:
            raise ValueError("Too few arguments to create a "
                             "multi dimensional array, pass dimensions.")
        if len(args) == 1:
            obj = Array.__new__(cls)
            obj._dtype = dtype
            obj._sizes = (args[0], 1)
            obj._data = [None] * args[0]
            return obj

        dimensions = args
        for dimension in dimensions:
            if dimension < 1:
                raise ValueError("Size of dimension cannot be less than 1")
        n_dimensions = len(dimensions)
        d_sizes = []
        index = 0
        while n_dimensions > 1:
            size = dimensions[index]
            for i in range(index+1,  len(dimensions)):
                size = size * dimensions[i]
            d_sizes.append(size)
            n_dimensions -= 1
            index += 1
        d_sizes.append(dimensions[index])
        d_sizes.append(1)
        obj = Array.__new__(cls)
        obj._dtype = dtype
        obj._sizes = tuple(d_sizes)
        obj._data = [None] * obj._sizes[1] * dimensions[0]
        return obj

    @classmethod
    def methods(cls) -> list:
        return ['__new__', '__getitem__', '__setitem__', 'fill', 'shape']

    def __getitem__(self, indices):
        self._compare_shape(indices)
        if isinstance(indices, int):
            return self._data[indices]
        position = 0
        for i in range(0, len(indices)):
            position += self._sizes[i + 1] * indices[i]
        return self._data[position]

    def __setitem__(self, indices, element) -> None:
        self._compare_shape(indices)
        if isinstance(indices, int):
            self._data[indices] = element
        else:
            position = 0
            for i in range(0, len(indices)):
                position += self._sizes[i + 1] * indices[i]
            self._data[position] = element

    def _compare_shape(self, indices) -> None:
        indices = [indices] if isinstance(indices, int) else indices
        if len(indices) != len(self._sizes) - 1:
            raise IndexError("Shape mismatch, current shape is %s" % str(self.shape))
        if any(indices[i] >= self._sizes[i] for i in range(len(indices))):
            raise IndexError("Index out of range.")

    def fill(self, element) -> None:
        element = self._dtype(element)
        for i in range(len(self._data)):
            self._data[i] = element

    @property
    def shape(self) -> tuple:
        shape = []
        size = len(self._sizes)
        for i in range(1, size):
            shape.append(self._sizes[i-1]//self._sizes[i])
        return tuple(shape)

class DynamicArray(Array):
    """
    Abstract class for dynamic arrays.
    """
    pass

class DynamicOneDimensionalArray(DynamicArray, OneDimensionalArray):
    """
    Represents resizable and dynamic one
    dimensional arrays.

    Parameters
    ==========

    dtype: type
        A valid object type.
    size: int
        The number of elements in the array.
    elements: list/tuple
        The elements in the array, all should
        be of same type.
    init: a python type
        The inital value with which the element has
        to be initialized. By default none, used only
        when the data is not given.
    load_factor: float, by default 0.25
        The number below which if the ratio, Num(T)/Size(T)
        falls then the array is contracted such that at
        most only half the positions are filled.
    backend: pydatastructs.Backend
        The backend to be used.
        Optional, by default, the best available
        backend is used.

    Raises
    ======

    ValueError
        When the number of elements in the list do not
        match with the size.
        More than three parameters are passed as arguments.
        Types of arguments is not as mentioned in the docstring.
        The load factor is not of floating point type.

    Note
    ====

    At least one parameter should be passed as an argument along
    with the dtype.
    Num(T) means the number of positions which are not None in the
    array.
    Size(T) means the maximum number of elements that the array can hold.

    Examples
    ========

    >>> from pydatastructs import DynamicOneDimensionalArray as DODA
    >>> arr = DODA(int, 0)
    >>> arr.append(1)
    >>> arr.append(2)
    >>> arr[0]
    1
    >>> arr.delete(0)
    >>> arr[0]
    >>> arr[1]
    2
    >>> arr.append(3)
    >>> arr.append(4)
    >>> [arr[i] for i in range(arr.size)]
    [None, 2, 3, 4, None, None, None]

    References
    ==========

    .. [1] http://www.cs.nthu.edu.tw/~wkhon/algo09/lectures/lecture16.pdf
    """

    __slots__ = ['_load_factor', '_num', '_last_pos_filled', '_size']

    def __new__(cls, dtype=NoneType, *args, **kwargs):
        backend = kwargs.get("backend", Backend.PYTHON)
        if backend == Backend.CPP:
            return _arrays.DynamicOneDimensionalArray(dtype, *args, **kwargs)
        obj = super().__new__(cls, dtype, *args, **kwargs)
        obj._load_factor = float(kwargs.get('load_factor', 0.25))
        obj._num = 0 if obj._size == 0 or obj[0] is None else obj._size
        obj._last_pos_filled = obj._num - 1
        return obj

    @classmethod
    def methods(cls):
        return ['__new__', '_modify',
        'append', 'delete', 'size',
        '__str__', '__reversed__']

    def _modify(self, force=False):
        """
        Contracts the array if Num(T)/Size(T) falls
        below load factor.
        """
        if force:
            i = -1
            while self._data[i] is None:
                i -= 1
            self._last_pos_filled = i%self._size
        if (self._num/self._size < self._load_factor):
            arr_new = OneDimensionalArray(self._dtype, 2*self._num + 1)
            j = 0
            for i in range(self._last_pos_filled + 1):
                if self._data[i] is not None:
                    arr_new[j] = self[i]
                    j += 1
            self._last_pos_filled = j - 1
            self._data = arr_new._data
            self._size = arr_new._size

    def append(self, el):
        if self._last_pos_filled + 1 == self._size:
            arr_new = OneDimensionalArray(self._dtype, 2*self._size + 1)
            for i in range(self._last_pos_filled + 1):
                arr_new[i] = self[i]
            arr_new[self._last_pos_filled + 1] = el
            self._size = arr_new._size
            self._data = arr_new._data
        else:
            self[self._last_pos_filled + 1] = el
        self._last_pos_filled += 1
        self._num += 1
        self._modify()

    def delete(self, idx):
        if idx <= self._last_pos_filled and idx >= 0 and \
            self[idx] is not None:
            self[idx] = None
            self._num -= 1
            if self._last_pos_filled == idx:
                self._last_pos_filled -= 1
            return self._modify()

    @property
    def size(self):
        return self._size

    def __str__(self):
        to_be_printed = ['' for _ in range(self._last_pos_filled + 1)]
        for i in range(self._last_pos_filled + 1):
            if self._data[i] is not None:
                to_be_printed[i] = str(self._data[i])
        return str(to_be_printed)

    def __reversed__(self):
        for i in range(self._last_pos_filled, -1, -1):
            yield self._data[i]

class ArrayForTrees(DynamicOneDimensionalArray):
    """
    Utility dynamic array for storing nodes of a tree.

    Parameters
    ==========

    backend: pydatastructs.Backend
        The backend to be used. Available backends: Python and C++
        Optional, by default, the Python backend is used. For faster execution, use the C++ backend.

    See Also
    ========

    pydatastructs.linear_data_structures.arrays.DynamicOneDimensionalArray
    """
    def _modify(self):
        if self._num/self._size < self._load_factor:
            new_indices = {}
            arr_new = OneDimensionalArray(self._dtype, 2*self._num + 1)
            j = 0
            for i in range(self._last_pos_filled + 1):
                if self[i] is not None:
                    arr_new[j] = self[i]
                    new_indices[self[i].key] = j
                    j += 1
            for i in range(j):
                if arr_new[i].left is not None:
                    arr_new[i].left = new_indices[self[arr_new[i].left].key]
                if arr_new[i].right is not None:
                    arr_new[i].right = new_indices[self[arr_new[i].right].key]
                if arr_new[i].parent is not None:
                    arr_new[i].parent = new_indices[self[arr_new[i].parent].key]
            self._last_pos_filled = j - 1
            self._data = arr_new._data
            self._size = arr_new._size
            return new_indices
        return None
