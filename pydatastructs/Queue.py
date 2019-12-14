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
	
    def __new__(self):
        self.elements = []

	def len(self):
        return len(self.elements)
    
    def append(self, elem):
   		self.elements.insert(0,elem)
  

	def popleft(self):
		self.elements.pop() 
    

