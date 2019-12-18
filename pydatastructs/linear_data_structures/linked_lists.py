from __future__ import print_function, division
from pydatastructs.utils.misc_util import _check_type, NoneType
from pydatastructs.utils import ( 
    Node
)

__author__ = 'rohansingh9001'

__all__ = [
    'DoublyLinkedList',
    'LinkedList'
]

class LinkedList(object):
    '''
    Abstract class for Linked List in pydatastructs.
    '''
    pass

# Class to create a Doubly Linked List 
class DoublyLinkedList(LinkedList): 
    

    '''
    A Doubly Linked List Class (abb. DLL)
    
    Parameters
    ==========
    
    None

    Examples
    ========
    >>> from pydatastructs import DoublyLinkedLIst as DLL
    >>> dll = DLL()
    >>> dll.append(6)
    >>> arr[0]
    6
    >>> dll.head
    6
    >>> dll.append(5)
    >>> dll.appendleft(2)
    >>> print(dll)
    [2,6,5]
    >>> dll[0] = 7.2
    >>> dll[0]
    7.2
    >>> dll.pop(1)
    6
    >>> print(dll)
    [2,5]

    References
    ==========
    
    https://www.geeksforgeeks.org/doubly-linked-list/

    '''
    __slots__ = ['head','tail','length']

    def __init__(self):
        self.head = NoneType
        self.tail = NoneType
        self.length = 0

    def appendleft(self,data):
        '''
        appendleft: 
        takes parameters - data
            data: type 
                A valid object type
                Should be convertible to string using str() method to 
                use print() method on instance.
        action - Pushes a new node at the start i.e. left of the DLL.
        '''
        self.length += 1
        newNode = Node(data)
        if self.head is not NoneType:
            self.head.prev = newNode
            newNode.next = self.head
        self.head = newNode

        if newNode.next == NoneType:
            self.tail = newNode
        if newNode.prev == NoneType:
            self.head = newNode
    
    def append(self, data):
        '''
        append: 
        takes parameters - data
            data: type
                A valid object type.
                Should be convertible to string using str() method to 
                use print() method on instance.
        action - Appends a new node at the end i.e. the right of the DLL.
        '''
        self.length += 1
        newNode = Node(data)
        if self.tail is not NoneType:
            self.tail.next = newNode
            newNode.prev = self.tail
        self.tail = newNode

        if newNode.next == NoneType:
            self.tail = newNode
        if newNode.prev == NoneType:
            self.head = newNode

    def insertAfter(self, prevNode, data):
        '''
        insertAfter:
        takes parameters - prevNode, data
            prevNode: Node type 
                An object of Node class 
            data: type
                A valid object type.
                Should be convertible to string using str() method to
                use print() method in instance.
        action - Inserts a new node after the prevNode.
        '''
        self.length += 1
        newNode = Node(data)
        newNode.next = prevNode.next
        prevNode.next = newNode
        newNode.prev = prevNode
        
        if newNode.next == NoneType:
            self.tail = newNode
        if newNode.prev == NoneType:
            self.head = newNode
    
    def insertBefore(self, nextNode, data):
        '''
        insertBefore:
        takes parameters - nextNode, data
            prevNode: Node type
                An object of Node class
            data: type
                A valid object type.
                Should be convertible to string using str() method to 
                use print() method in instance.
        action - Inserts a new node before the newNode.
        '''
        self.length += 1
        newNode = Node(data)
        newNode.prev = nextNode.prev
        nextNode.prev = newNode
        newNode.next = nextNode
        
        if newNode.next == NoneType:
            self.tail = newNode
        if newNode.prev == NoneType:
            self.head = newNode
    
    def insertAt(self, index, data):
        '''
        insertAt:
        takes parameters - index, data
            index: int type
                An integer i such that 0<= i <= length, where length 
                refers to the length of the List.
            data: type
                A valid object type.
                Should be convertible to string using str() method to
                use print() method in instance.
        action - Inserts a new node at the input index.
        '''
        if index > self.length or index < 0 or not (_check_type(index, int)):
            raise ValueError('Index input out of range/Index is expected to be an Integer.')
        else:
            if index == 0:
                self.appendleft(data)
            elif index == self.length:
                self.appendright(data)
            else:  
                self.length += 1
                newNode = Node(data)
                counter = 0
                currentNode = self.head
                while counter != index:
                    currentNode = currentNode.next
                    counter += 1
                currentNode.prev.next = newNode
                newNode.prev = currentNode.prev
                currentNode.prev = newNode
                newNode.next = currentNode
                    
                if newNode.next == NoneType:
                    self.tail = newNode
                if newNode.prev == NoneType:
                    self.head = newNode
    
    def popleft(self):
        '''
        popleft: 
        takes parameters - None
        action - Removes the Node from the left i.e. start of the DLL
         and returns the data from the Node.
        '''
        self.length -= 1
        oldHead = self.head
        oldHead.next.prev = NoneType
        self.head = oldHead.next
        return oldHead.data 

    def popright(self):
        '''
        popright:
        takes parameters - None
        action - Removes the Node from the right i.e. end of the DLL 
        and returns the data from the Node.
        '''
        self.length -= 1
        oldTail = self.tail
        oldTail.prev.next = NoneType
        self.tail = oldTail.prev
        return oldTail.data

    def pop(self, index=0):
        '''
        pop:
        takes parameters - index
            index: int type
                An integer i such that 0<= i <= length, where length
                 refers to the length of the List.
        action - Removes the Node at the index of the DLL and returns
         the data from the Node.
        '''
        if index > self.length or index < 0 or not (_check_type(index, int)):
            raise ValueError('Index input out of range/Index is expected to be an Integer.') 
        else:  
            if index == 0:
                self.popleft()
            elif index == self.length:
                self.popright()
            else:
                self.length -= 1
                counter = 0
                currentNode = self.head
                while counter != index:
                    currentNode = currentNode.next
                    counter += 1
                currentNode.prev.next = currentNode.next
                currentNode.next.prev = currentNode.prev
                return currentNode.data

    def __getitem__(self, index): 
        '''
        __getitem__:
        takes parameters - index
            index: int type
                An integer i such that 0<= i <= length, where length 
                refers to the length of the List.
        action - Returns the data of the Node at index.
        '''
        if index > self.length or index < 0 or not (_check_type(index, int)):
            raise ValueError('Index input out of range/Index is expected to be an Integer.')
        else:     
            counter = 0
            currentNode = self.head      
            while counter != index:
                currentNode = currentNode.next
                counter += 1
            return currentNode.data

    def __setitem__(self, index, data):
        '''
        __setitem__:
        takes parameters - index, data
            index: int type
                An integer i such that 0<= i <= length, where length 
                refers to the length of the List.
            data: type
                A valid object type.
                Should be convertible to string using str() method to use 
                print() method in instance.
        action - Sets the data of the Node at the index to the input data.
        '''
        if index > self.length or index < 0 or not (_check_type(index, int)):
            raise ValueError('Index input out of range/Index is expected to be an Integer.')
        else:  
            counter = 0
            currentNode = self.head    
            while counter != index:
                currentNode = currentNode.next
                counter += 1
            currentNode.data = data

    def __str__(self):
        '''
        __str__:
        takes parameters - None
        action - Prints the DLL in a list from from the start to the end.
        '''
        elements = []
        currentNode = self.head
        while currentNode is not NoneType:
            elements.append(currentNode.data)
            currentNode = currentNode.next
        return str(elements)

    def __len__(self):
        '''
        __len__:
        takes parameters - None
        action - Returns the length of the DLL.
        '''
        return self.length

    def isEmpty(self):
        '''
        isEmpty:
        takes parameters - None
        action - Return a bool value to check if the DLL is empty or not.
        '''
        return self.length == 0

if __name__ == '__main__':
    dll = DoublyLinkedList()
    dll.append(6)
    arr[0]
    dll.head
    dll.append(5)
    dll.appendleft(2)
    print(dll)
    dll[0] = 7.2
    dll[0]
    dll.pop(1)
    print(dll)