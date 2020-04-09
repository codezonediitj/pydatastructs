from pydatastructs.utils.misc_util import _check_type, NoneType

__all__ = [
    'OneDimensionalArray',
    'MultiDimensionalArray',
    'DynamicOneDimensionalArray'
]


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
    elements: list
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

    __slots__ = ['_size', '_data', '_dtype']

    def __new__(cls, dtype=NoneType, *args, **kwargs):
        if dtype is NoneType or len(args) not in (1, 2):
            raise ValueError("1D array cannot be created due to incorrect"
                             " information.")
        obj = Array.__new__(cls)
        obj._dtype = dtype
        if len(args) == 2:
            if _check_type(args[0], list) and \
                    _check_type(args[1], int):
                for i in range(len(args[0])):
                    if dtype != type(args[0][i]):
                        args[0][i] = dtype(args[0][i])
                size, data = args[1], [arg for arg in args[0]]
            elif _check_type(args[1], list) and \
                    _check_type(args[0], int):
                for i in range(len(args[1])):
                    if dtype != type(args[1][i]):
                        args[1][i] = dtype(args[1][i])
                size, data = args[0], [arg for arg in args[1]]
            else:
                raise TypeError("Expected type of size is int and "
                                "expected type of data is list/tuple.")
            if size != len(data):
                raise ValueError("Conflict in the size %s and length of data %s"
                                 % (size, len(data)))
            obj._size, obj._data = size, data

        elif len(args) == 1:
            if _check_type(args[0], int):
                obj._size = args[0]
                init = kwargs.get('init', None)
                obj._data = [init for i in range(args[0])]
            elif _check_type(args[0], (list, tuple)):
                for i in range(len(args[0])):
                    if dtype != type(args[0][i]):
                        args[0][i] = dtype(args[0][i])
                obj._size, obj._data = len(args[0]), \
                                       [arg for arg in args[0]]
            else:
                raise TypeError("Expected type of size is int and "
                                "expected type of data is list/tuple.")

        return obj

    def __getitem__(self, i):
        if i >= self._size or i < 0:
            raise IndexError("Index out of range.")
        return self._data.__getitem__(i)

    def __setitem__(self, idx, elem):
        if elem is None:
            self._data[idx] = None
        else:
            if type(elem) != self._dtype:
                elem = self._dtype(elem)
            self._data[idx] = elem

    def fill(self, elem):
        elem = self._dtype(elem)
        for i in range(self._size):
            self._data[i] = elem


class MultiDimensionalArray(Array):
    '''
        Represents a multi-dimensional array.

        Parameters
        ==========

        dtype: type
            A valid object type.
        size: int
            The number of elements in the array.

        Raises
        ======

        ValueError
            When the number of elements in the list do not
            match with the size.
            More than three parameters are passed as arguments.
            Types of arguments is not as mentioned in the docstring.

        Note
        ====


        Examples
        ========
        x = MultiDimensionalArray(int, 3,4,5)

        x.fill(32)
        print(x)
        print(x._data)
        for y in x:
            print("y: ", y._data)
            for z in y:
                print("z: ", z._data)
        >>> from pydatastructs import MultiDimensionalArray as MDA
        >>> arr = MDA(int, 5, 6, 9)
        >>> arr.fill(32)
        >>> arr[3][0][0]
        32
        >>> arr[3][0][0] = 7.2
        >>> arr[3][0][0]
        7

        References
        ==========

        .. [1] https://en.wikipedia.org/wiki/Array_data_structure#Multidimensional_arrays
        '''
    __slots__ = ['_size', '_data', '_dtype']

    def __new__(cls, dtype=NoneType, *args, **kwargs):
        if dtype is NoneType or len(args) == (0):
            raise ValueError("array cannot be created due to incorrect"
                             " information.")
        dimensiones = list(args)

        if dtype == MultiDimensionalArray:
            # # its an array of arrays
            obj = Array.__new__(cls)
            obj._dtype = MultiDimensionalArray
            obj._size = dimensiones[0]
            obj._data = [None] * obj._size

            return obj
        elif dtype == OneDimensionalArray:
            obj = Array.__new__(cls)
            obj._dtype = OneDimensionalArray
            obj._size = dimensiones[0]
            obj._data = [None] * obj._size

            return obj
            pass
        else:

            # Initialization of array
            i = len(dimensiones) - 1
            array = OneDimensionalArray(dtype, dimensiones[i])
            i -= 1
            while (i >= 0):
                new_array = MultiDimensionalArray(OneDimensionalArray, dimensiones[i])
                for j in range(new_array._size):
                    new_array._data[j] = array
                array = new_array
                i -= 1

        return array

    def __getitem__(self, idx):
        # return list
        if idx >= self._size or idx < 0:
            raise IndexError("Index out of range.")
        return self._data.__getitem__(idx)

    def __setitem__(self, idx, element):
        if idx >= self._size or idx < 0:
            raise IndexError("Index out of range.")
        if type(element) != self._data[0]._dtype:
            raise TypeError("Unexpected item type.")
        # Check the size of the element if it is, set it
        if self.compare_size(element):
            self._data[idx] = element
        else:
            raise TypeError("Unexpected item type.")

    def compare_size(self, array):
        if self._data[0]._size == array._size:
            if array._dtype == MultiDimensionalArray:
                return self._data[0].compare_size(array)
            elif array._dtype == OneDimensionalArray:
                if array[0]._dtype == self._data[0][0]._dtype:
                    return True
        return False

    def fill(self, element):
        element
        for i in range(self._size):
            self._data[i].fill(element)
            # self.__setitem__(i, element)


ODA = OneDimensionalArray


class DynamicArray(Array):
    """
    Abstract class for dynamic arrays.
    """
    pass


class DynamicOneDimensionalArray(DynamicArray, OneDimensionalArray):
    """
    Represents dynamic one dimensional arrays.

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
        obj = super().__new__(cls, dtype, *args, **kwargs)
        obj._load_factor = float(kwargs.get('load_factor', 0.25))
        obj._num = 0 if obj._size == 0 or obj[0] is None else obj._size
        obj._last_pos_filled = obj._num - 1
        return obj

    def _modify(self):
        """
        Contracts the array if Num(T)/Size(T) falls
        below load factor.
        """
        if self._num / self._size < self._load_factor:
            arr_new = ODA(self._dtype, 2 * self._num + 1)
            j = 0
            for i in range(self._last_pos_filled + 1):
                if self[i] is not None:
                    arr_new[j] = self[i]
                    j += 1
            self._last_pos_filled = j - 1
            self._data = arr_new._data
            self._size = arr_new._size

    def append(self, el):
        if self._last_pos_filled + 1 == self._size:
            arr_new = ODA(self._dtype, 2 * self._size + 1)
            for i in range(self._last_pos_filled + 1):
                arr_new[i] = self[i]
            arr_new[self._last_pos_filled + 1] = el
            self._last_pos_filled += 1
            self._size = arr_new._size
            self._num += 1
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


class ArrayForTrees(DynamicOneDimensionalArray):
    """
    Utility dynamic array for storing nodes of a tree.

    See Also
    ========

    pydatastructs.linear_data_structures.arrays.DynamicOneDimensionalArray
    """

    def _modify(self):
        if self._num / self._size < self._load_factor:
            new_indices = dict()
            arr_new = OneDimensionalArray(self._dtype, 2 * self._num + 1)
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


def main():
    x = MultiDimensionalArray(int, 3, 4, 5)

    x.fill(32)
    print(x)
    print(x._data)
    for y in x:
        print("y: ", y._data)
        for z in y:
            print("z: ", z._data)


if __name__ == "__main__":
    main()
