from pydatastructs.linear_data_structures import DynamicOneDimensionalArray

__all__ = [
    'Queue'
]

_check_type = lambda a, t: isinstance(a, t)
NoneType = type(None)
rear= -1

class Queue(objects):
    def __new__(clas, implementation='array', **kwargs):
        if implementation == 'array':
            return ArrayQueue(
                kwargs.get('maxsize', None),
                kwargs.get('front', -1),
                kwargs.get('item', None),
                kwargs.get('dtype', int),
                kwargs.get('count', int))
        raise NotImplementedError("%s hasn't been implemented yet."%(implementation))
               
   def append(self, *args, **kwargs):
        raise NotImplementedError("This is an abstract method.")
        
   def popleft(self, **kwargs):
        raise NotImplementedError("This is an abstract method.")
        
   def __len__(self, **kwargs):
        raise NotImplementedError("This is an abstract method.")
        
   
class ArrayQueue(Queue):
    __slots__ = ['maxsize','front','item','dtype','count']
    def __new__(clas, maxsize = None, front = -1, item = None, dtype = int, count=0):
        if not _check_type(maxsize, int):
            raise ValueError("maxsize is missing.")
        if not _check_type(front, int):
            raise TypeError("front is not of type int.")
        if item is None:
            item= DynamicOneDimensionalArray(dtype, maxsize)
        if not _check_type(item, DynamicOneDimensionalArray):
            raise ValueError("item is not of DynamicOneDimensionalArray type")
            
        obj = object.__new__(clas)
        obj.maxsize, obj.front, obj.item, obj.dtype, obj.count = maxsize, front, item, items._dtype, count
        return obj
        
    def append(self, x):
            if self.front == -1:
                self.front=0
            self.item.apped[self.dtype(x)]
            count+=1

    def popleft(self):
        if (self.front == -1):
            raise ValueError("Queue is empty.")
        r = self.item[self.front]
        self.item.delete[self.front]
        self.front += 1
        return r
        
    def __len__(self):
        if self.front== -1:
            return 0
        else:
            return (self.count- self.front)
