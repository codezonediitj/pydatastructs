from __future__ import print_function, division

_check_type = lambda a, t: isinstance(a, t)

__all__ = [
'OneDimensionalArray'
]

class Array(object):
    """
    Abstract class for arrays in pydatastructs.
    """
    pass

class OneDimensionalArray(Array):
    """
    Represents one dimensional arrays.

    Parameters
    ==========

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
    TypeError
        When all the elements are not of same type.

    Note
    ====

    At least one parameter should be passed as an argument.

    Examples
    ========
    """
    __slots__ = ['_size', '_data']

    def __new__(cls, *args, **kwargs):
        if not args or len(args) not in (1, 2):
            raise ValueError("1D array cannot be created due to incorrect"
                                " information.")
        obj = object.__new__(cls)
        if len(args) == 2:
            if _check_type(args[0], (list, tuple)) and \
                _check_type(args[1], int):
                size, data = args[1], args[0]
            elif _check_type(args[1], (list, tuple)) and \
                _check_type(args[0], int):
                size, data = args[0], args[1]
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
                obj._size, obj._data = len(args[0]), args[0]
            else:
                raise TypeError("Expected type of size is int and "
                                "expected type of data is list/tuple.")

        return obj
