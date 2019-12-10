from pydatastructs.utils.misc_util import _check_type

NoneType = type(None)

__all__ = ['binaryHeap']

class binaryHeap():
    """Respresentation of BinaryHeap data structure

    Parameters
    ==========

    array : list
        Optional, by default 'None'
        List of initial elements in Heap
    _type : str
        Type of Heap.
        Takes 'min' or 'max'
        By default 'min'
    
    References
    ==========

    .. [1] https://en.m.wikipedia.org/wiki/Binary_heap
    """
    def __new__(cls, array=None, _type="min"):
        if _type=="min":
            return MinHeap(array)
        elif _type=="max":
            return MaxHeap(array)
        else:
            raise NotImplementedError("%s hasn't been implemented yet."%(_type))
    
    def insert(self, *args, **kwargs):
        """
        Insert a new element to the Heap according to heap property.

        Parameters
        ==========

        new_key: float
            A real number.
        
        """
        raise NotImplementedError(
            "This is an abstract method.")

    def extract(self):
        """
        Extract root element of the Heap.

        Returns
        ==========
        
        element_to_be_extracted : float
            Min or Max of Heap according to type of Heap.
        
        """
        raise NotImplementedError(
              "This is an abstract method.")    
    
    
        
class MinHeap(binaryHeap):
    """
    Represents MinHeap.

    Example
    =======

    >>> from pydatastructs.trees.heaps import binaryHeap
    >>> h = binaryHeap()
    >>> h.insert(1)
    >>> h.insert(5)
    >>> h.insert(7)
    >>> h.extract()
    1
    >>> h.insert(4)
    >>> h.extract()
    4
    
    """
    
    
    __slots__ = ['_last_pos_filled']
    
    def __new__(cls,array):
        obj = object.__new__(cls)
        if _check_type(array,NoneType):
            obj.array = []
        else:
            obj.array=array
        obj._last_pos_filled=len(obj.array)-1
        obj.__build()
        return obj
    
    def __heapify(self,i):
        minimum=i
        l=2*i+1
        r=2*i+2
        
        if l<=self._last_pos_filled:
            minimum = l if self.array[l]<self.array[minimum] else i
        if r<=self._last_pos_filled:
            minimum = r if self.array[r]<self.array[minimum] else minimum
        
        if minimum!=i:
            self.array[minimum], self.array[i]=self.array[i], self.array[minimum]
            i = minimum
            self.__heapify(i)
    
    def __build(self):
        for i in range(len(self.array)//2,-1,-1):
            self.__heapify(i)        
            
    def insert(self,new_key):
        self.array.append(new_key)
        self._last_pos_filled+=1
        i=self._last_pos_filled
        
        while(True):
            parent = (i-1)//2
            if i==0 or self.array[parent]<self.array[i]:
                break
            else:
                self.array[parent], self.array[i] = self.array[i], self.array[parent]
                i = parent
                

    
    def extract(self):
        element_to_be_extracted = self.array[0]
        self.array[0] = self.array[self._last_pos_filled]
        self.array[self._last_pos_filled] = float('inf')
        self.__heapify(0)
        self.array.pop(self._last_pos_filled)
        self._last_pos_filled-=1
        return element_to_be_extracted


class MaxHeap(binaryHeap):
    """
    Represents MinHeap.

    Example
    =======

    >>> from pydatastructs.trees.heaps import binaryHeap
    >>> h = binaryHeap(_type='max')
    >>> h.insert(1)
    >>> h.insert(5)
    >>> h.insert(7)
    >>> h.extract()
    7
    >>> h.insert(6)
    >>> h.extract()
    6
    
    """
    
    __slots__ = ['_last_pos_filled']
    
    def __new__(cls,array):
        obj = object.__new__(cls)
        if type(array) is type(None):
            obj.array = []
        else:
            obj.array=array
        obj._last_pos_filled=len(obj.array)-1
        obj.__build()
        return obj
    
    def __heapify(self,i):
        maximum=i
        l=2*i+1
        r=2*i+2
        
        if l<=self._last_pos_filled:
            maximum = l if self.array[l]>self.array[maximum] else i
        if r<=self._last_pos_filled:
            maximum = r if self.array[r]>self.array[maximum] else maximum
        
        if maximum!=i:
            self.array[maximum], self.array[i]=self.array[i], self.array[maximum]
            i = maximum
            self.__heapify(i)
    
    def __build(self):
        for i in range(len(self.array)//2,-1,-1):
            self.__heapify(i)        
            
    def insert(self,new_key):
        self.array.append(new_key)
        self._last_pos_filled+=1
        i=self._last_pos_filled
        
        while(True):
            parent = (i-1)//2
            if i==0 or self.array[parent]>=self.array[i]:
                break
            else:
                self.array[parent], self.array[i] = self.array[i], self.array[parent]
                i = parent
                    
    def extract(self):
        element_to_be_extracted = self.array[0]
        self.array[0] = self.array[self._last_pos_filled]
        self.array[self._last_pos_filled] = float('-inf')
        self.__heapify(0)
        self.array.pop(self._last_pos_filled)
        self._last_pos_filled-=1
        return element_to_be_extracted