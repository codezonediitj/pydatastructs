# API to create N dimensional Array
'''
Data Members
1. _ndim - The number of dimensions in the array.
2. _data - The python list which will store the data in row major order.
3. _dtype - The data type of the elements.

Methods
1. __new__(cls, dtype=NoneType, *args, **kwargs)
2. __getitem__(self, *indices)
3. __setitem__(self, value, *indices)
4. fill(self, elem)

'''
from pydatastructs.utils.misc_util import _check_type, NoneType

__all__ = [
'OneDimensionalArray',
'DynamicOneDimensionalArray',
'MutiDimensionalArray'
]

class Array(object):
    '''
    Abstract class for arrays in pydatastructs.
    '''
    pass


class MutiDimensionalArray(Array):

    def __new__(cls, dtype=NoneType, *args, **kwargs):
        obj = object.__new__(cls)
        obj._ndim = [None]
        self._data = [None]
        self._dtype = dtype
        
        
    def __getitem__(self, *indices):
        #get indices and form a matrix
        #create a m x n matrix
        m = indices[0]
        n = indices[1]
        a = [[0 for x in range(n)] for x in range(m)] 
        
        
    def __setitem__(self, m, n, *indices_value):
        # to get updated values of an index and update the index
        value = indices_value[-1]
        # update elem
        if value is None:
            self._data[m][n] = None
        else:
            if type(value) != self._dtype:
                value = self._dtype(value)
            self._data[m][n] = value
    
    def fill(self, m ,n, elem):
        # fill all the updated incides in n-d array
        elem = self._dtype(elem)
        for i in range(m):
            for j in range (n)
                self._data[i][j] = elem
