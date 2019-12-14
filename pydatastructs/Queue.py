from __future__ import print_function
class Queue:
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
        self.elements = []

	def len(self):
        return len(self.elements)
    
	def isEmpty(self):
        return self.elements == []

    def isFull(self):
    	if len(self.elements)<self.max_size 
    		return 0 
    	else return 1

    def append(self, elem):
    	if (isFull(self)!=0)
    		self.elements.insert(0,elem)
    	else raise Error("Unable to acess memory segment")

	def popleft(self):
        if isEmpty(self)
        	 return "Queue empty"
        else self.elements.pop() 
    

