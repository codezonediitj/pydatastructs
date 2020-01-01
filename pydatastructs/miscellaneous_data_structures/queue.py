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
                kwargs.get('front', -1),
                kwargs.get('item', None),
                kwargs.get('dtype', int))
        raise NotImplementedError("%s hasn't been implemented yet."%(implementation))
               
   def append(self, *args, **kwargs):
        raise NotImplementedError("This is an abstract method.")
        
   def popleft(self, **kwargs):
        raise NotImplementedError("This is an abstract method.")
        
        
class ArrayQueue(Queue):
    __slots__ = ['front','item','dtype','count']
    def __new__(clas, front = -1, item = None, dtype = int):
        if not _check_type(front, int):
            raise TypeError("front is not of type int.")
        if item is None:
            item= DynamicOneDimensionalArray(dtype, 0)
        else:
            item= DynamicOneDimensionalArray(dtype, item)
            
        obj = object.__new__(clas)
        obj.front, obj.item, obj.dtype = front, item, items._dtype
        return obj
        
    def append(self, x):
            if self.front == -1:
                self.front=0
            self.item.append(x)

    def popleft(self):
        if (self.front == -1):
            raise ValueError("Queue is empty.")
        r = dc(self.item[self.front])
        self.item.delete(self.front)
        self.front += 1
        return r
        
    def __str__(self):
        """
        Used for printing.
        """
        return str(self.item._data)
