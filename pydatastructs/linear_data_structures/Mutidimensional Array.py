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

class MutiDimensionalArray(object):

    def __new__(cls, dtype=NoneType, *args, **kwargs):
        obj = object.__new__(cls)
        obj._ndim = [None]
        self._data = [None]
        self._dtype = dtype
        
        
    def __getitem__(self, *indices):
        #get indices and form a matrix
        #create a m x n matrix
        a = [[0 for x in range(n)] for x in range(m)] 
        
    def __setitem__(self, value, *indices):
        # to get updated values of an index and update the index
        pass
    
    def fill(self, elem):
        # fill all the updated incides in n-d array
        pass
