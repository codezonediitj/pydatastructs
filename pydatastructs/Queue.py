from __future__ import print_function
from __




class Queue():
	'''
	Creation of Queue Data Type in python with list prebuilt data type
	------------------------------------------------------------------

	Parameter
	==========
	max_size:
		 type-int.
		 denotes the maximum size of queue.
	

	Raises
	=======
	No particular raisse till now.

	Operations available:
	=====================
	1. initialisation of queue.
	2. Check whether Queue is empty or not.
	3. Appending elements into the queue on a first come first serve basis.
	4. popping elements on first arrival basis.
	5. detecting length of Queue.
	6. Check whether queue is full or not.
	 
	'''
    def __init__(self):
        self.elem = []

	"""isEmpty()-check whether Queue is empty or not"""
    def isEmpty(self):
        return self.elem == []
    """isFull()-check status of queue whether it is full or not"""
    def isFull(self):
    	if len(self.elem)<self.elem.max_size 
    		return 0
    	else return 1;

	"""append()-entering the first element of a queue"""
    def append(self, elem):
    	if isFull(self)!=0
    		self.elem.insert(0,elem)
    	else raise Error("Variable storage failure")

	"""popleft()-popping out the first element that has
 	entered the queue according to the FIFO concept"""
	def popleft(self):
        if self.elem.isFull(self)
        	return self.elem.pop()


	"""len()-returns length of a queue"""
    def len(self):
        return len(self.elem)

