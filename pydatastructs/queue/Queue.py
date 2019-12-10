class Queue:
    def __init__(self):
        self.elem = []

    def isEmpty(self):
        return self.elem == []
"""append()-entering the first element of a queue"""
    def append(self, elem):
        self.elem.insert(0,elem)

"""popleft()-popping out the first element that has entered the queue according to the FIFO concept"""
	def popleft(self):
        return self.elem.pop()
"""len-returns length of a queue"""
    def size(self):
        return len(self.elem)

