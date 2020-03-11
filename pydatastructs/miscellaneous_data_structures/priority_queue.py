from heapq import heapify,heappush,heappop

__all__ = [
    "PriorityQueue"
]
class PriorityQueue(object):
    """
    Representation of PriorityQueue Data Structure
    Parameters
    ==========
    implementation : str
        Implementation to be used for queue.
        By default, 'BinaryHeap'
    items : list/tuple
        Optional, by default, None
        The inital items in the Priority Queue.
    dtype : A valid python type
        Optional, by default int if item
        is int.
    Examples
    ========
    >>> from pydatastructs import PriorityQueue
    >>> q = PriorityQueue()
    >>> q.insert(2)
    >>> q.insert(1)
    >>> q.insert(3)
    >>> q.getHighestPriority()
    3
    >>> print(q)
    1 2 3

    References
    ==========
    .. [1] https://en.wikipedia.org/wiki/Priority_queue
       [2] https://www.geeksforgeeks.org/priority-queue-set-1-introduction
    """
    def __new__(cls,implementation="BinaryHeap",**kwargs):
        if implementation=="BinaryHeap":
            return BinaryHeapPQ(
                kwargs.get('items',None),
                kwargs.get('dtype',int)
            )
        raise NotImplementedError("%s has not been implemented yet!"%(implementation))

    def insert(self):
        raise NotImplementedError("%s has not been implemented yet!"%(implementation))

    def getHighestPriority(self):
        raise NotImplementedError("%s has not been implemented yet!"%(implementation))

    def deleteHighestPriority(self):
        raise NotImplementedError(" %s has not been implemented yet!"%(implementation))

    @property
    def is_empty(self):
        raise NotImplementedError("Abstract Property !")

class BinaryHeapPQ(PriorityQueue):

    __slots__ = [
        "items"
        ]
    def __new__(cls,items=None,dtype=int):
        items = object.__new__(cls)
        items.heap = []
        heapify(items.heap)
        return items

    def insert(self,k):
        heappush(self.heap,k)

    def getHighestPriority(self,priority="max"):
        if priority=="max":
            max_ = max(self.heap)
            return max_
        elif priority=="min":
            min_ = min(self.heap)
            return min_

    def parentkey(self,i):
        return (i-1)//2

    def decreaseKey(self,i,new_val):
        self.heap[i] = new_val
        while(i!=0 and self.heap[self.parentkey(i)]>self.heap[i]):
            self.heap[i],self.heap[self.parentkey(i)] = self.heap[self.parentkey(i)],self.heap[i]

    def deleteHighestPriority(self,priority="max"):
        if priority=="max":
            max_ = max(self.heap)
            max_index = self.heap.index(max_)
            self.decreaseKey(max_index,float('-inf'))
            heappop(self.heap)
            return max_
        elif priority=="min":
            min_ = self.heap[0]
            heappop(self.heap)
            return min_

    def __str__(self):
        "Used to Print Binary Heap of Priority Queue"
        return " ".join([str(i) for i in self.heap])

    @property
    def is_empty(self):
        return self.heap==[]
