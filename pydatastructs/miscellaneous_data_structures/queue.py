from pydatastructs.linear_data_structures import OneDimensionalArray

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
                kwargs.get('rear', -1),
                kwargs.get('item', None),
                kwargs.get('dtype', int))
        raise NotImplementedError("%s hasn't been implemented yet."%(implementation))
               
   def append(self, *args, **kwargs):
        raise NotImplementedError("This is an abstract method.")
        
   def popleft(self, **kwargs):
        raise NotImplementedError("This is an abstract method.")
        
   def __len__(self, **kwargs):
        raise NotImplementedError("This is an abstract method.")
        
   
class ArrayQueue(Queue):
    __slots__ = ['maxsize','front','rear','item','dtype']
    def __new__(cls, maxsize = None, front = -1, rear = -1, item = None, dtype = int):
        if not _check_type(maxsize, int):
            raise ValueError("maxsize is missing.")
        if not _check_type(front, int):
            raise TypeError("front is not of type int.")
        if not _check_type(rear, int):
            raise TypeError("rear is not of type int.")
        if item is None:
            item= OneDimensionalArray(dtype, maxsize)
        if not _check_type(item, OneDimensionalArray):
            raise ValueError("item is not of OneDimensionalArray type")
        if item._size > maxsize:
            raise ValueError("Overflow, size of item %s is greater than maxsize, %s"%(items._size, maxsize))
            
        obj = object.__new__(clas)
        obj.maxsize, obj.front, obj.rear, obj.item, obj.dtype = maxsize, front, rear, item, items._dtype
        return obj
        
    def append(self, x):
        if self.rear == self.maxsize-1:
            raise ValueError("Queue is full.")
        else:
            if self.front == -1:
                self.front=0
            self.rear +=1
            self.item[self.rear]= self.dtype(x)

    def popleft(self):
        if (self.front == -1) and (self.front > self.rear):
            raise ValueError("Queue is empty.")
        self.top -= 1
        r = self.item[self.front]
        self.item[self.front] = None
        self.front += 1
        return r
        
    def __len__(self):
        i=0
        count=0
        while(self.item[i] is not None):
            i+=1
            count+=1
        return count
