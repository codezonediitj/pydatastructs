from __future__ import print_function, division

__all__ = [
'OneDimensionalArray'
]

_check_type = lambda a, t: isinstance(a, t)
NoneType = type(None)

class Array(object):
    '''
    Abstract class for arrays in pydatastructs.
    '''
    pass

class OneDimensionalArray(Array):
    '''
    Represents one dimensional arrays.

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

    >>> from pydatastructs import OneDimensionalArray as ODA
    >>> arr = ODA(int, 5)
    >>> arr.fill(6)
    >>> arr[0]
    6
    >>> arr[0] = 7.2
    >>> arr[0]
    7

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Array_data_structure#One-dimensional_arrays
    '''
    def __new__(cls, dtype=NoneType, *args, **kwargs):
        if dtype == NoneType or len(args) not in (1, 2):
            raise ValueError("1D array cannot be created due to incorrect"
                                " information.")
        obj = object.__new__(cls)
        obj._dtype = dtype
        if len(args) == 2:
            if _check_type(args[0], (list, tuple)) and \
                _check_type(args[1], int):
                size, data = args[1], [dtype(arg) for arg in args[0]]
            elif _check_type(args[1], (list, tuple)) and \
                _check_type(args[0], int):
                size, data = args[0], [dtype(arg) for arg in args[1]]
            else:
                raise TypeError("Expected type of size is int and "
                                "expected type of data is list/tuple.")
            if size != len(data):
                raise ValueError("Conflict in the size %s and length of data %s"
                                 %(size, len(data)))
            obj._size, obj._data = size, data

        elif len(args) == 1:
            if _check_type(args[0], int):
                obj._size = args[0]
                init = kwargs.get('init', None)
                obj._data = [init for i in range(args[0])]
            elif _check_type(args[0], (list, tuple)):
                obj._size, obj._data = len(args[0]), \
                                        [dtype(arg) for arg in args[0]]
            else:
                raise TypeError("Expected type of size is int and "
                                "expected type of data is list/tuple.")

        return obj

    def __getitem__(self, i):
        if i >= self._size or i < 0:
            raise IndexError("Index out of range.")
        return self._data.__getitem__(i)

    def __setitem__(self, idx, elem):
        self._data[idx] = self._dtype(elem)

    def fill(self, elem):
        elem = self._dtype(elem)
        for i in range(self._size):
            self._data[i] = elem
