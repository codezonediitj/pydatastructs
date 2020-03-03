from pydatastructs import SinglyLinkedList

class Linked_Stacks:
    
    # A class to implement Stacks Built over Singly Linked Lists
    
    def __init__(self):
        self.sll = SinglyLinkedList()
        self.top = self.sll.head
    
    def push(self,data):
        self.sll.append(data)
        if self.top is None:
            self.top = self.sll.head
        return self

    def pop(self):
        if self.top is not None:
            self.data = self.top.data
            self.top = self.top.next
        return self.data
    
    def peek(self):
        return self.top.data