# Python3 code for inserting element in skip list 
  
import random 
  
class Node(object): 
    ''' 
    Class to implement node 
    '''
    def __init__(self, key, level): 
        self.key = key 
  
        # list to hold references to node of different level  
        self.forward = [None]*(level+1) 
  
class SkipList(object): 
    ''' 
    Class for Skip list 
    '''
    def __init__(self, max_lvl, P): 
        # Maximum level for this skip list 
        self.MAXLVL = max_lvl 
  
        # P is the fraction of the nodes with level  
        # i references also having level i+1 references 
        self.P = P 
  
        # create header node and initialize key to -1 
        self.header = self.createNode(self.MAXLVL, -1) 
  
        # current level of skip list 
        self.level = 0
      
    # create  new node 
    def createNode(self, lvl, key): 
        n = Node(key, lvl) 
        return n 
      
    # create random level for node 
    def randomLevel(self): 
        lvl = 0
        while random.random()<self.P and \ 
              lvl<self.MAXLVL:lvl += 1
        return lvl 
  
    # insert given key in skip list 
    def insertElement(self, key): 
        # create update array and initialize it 
        update = [None]*(self.MAXLVL+1) 
        current = self.header 
  
        ''' 
        start from highest level of skip list 
        move the current reference forward while key  
        is greater than key of node next to current 
        Otherwise inserted current in update and  
        move one level down and continue search 
        '''
        for i in range(self.level, -1, -1): 
            while current.forward[i] and \ 
                  current.forward[i].key < key: 
                current = current.forward[i] 
            update[i] = current 
  
        '''  
        reached level 0 and forward reference to  
        right, which is desired position to  
        insert key. 
        ''' 
        current = current.forward[0] 
  
        ''' 
        if current is NULL that means we have reached 
           to end of the level or current's key is not equal 
           to key to insert that means we have to insert 
           node between update[0] and current node 
       '''
        if current == None or current.key != key: 
            # Generate a random level for node 
            rlevel = self.randomLevel() 
  
            ''' 
            If random level is greater than list's current 
            level (node with highest level inserted in  
            list so far), initialize update value with reference 
            to header for further use 
            '''
            if rlevel > self.level: 
                for i in range(self.level+1, rlevel+1): 
                    update[i] = self.header 
                self.level = rlevel 
  
            # create new node with random level generated 
            n = self.createNode(rlevel, key) 
  
            # insert node by rearranging references  
            for i in range(rlevel+1): 
                n.forward[i] = update[i].forward[i] 
                update[i].forward[i] = n 
  
            print("Successfully inserted key {}".format(key)) 
  
    # Display skip list level wise 
    def displayList(self): 
        print("\n*****Skip List******") 
        head = self.header 
        for lvl in range(self.level+1): 
            print("Level {}: ".format(lvl), end=" ") 
            node = head.forward[lvl] 
            while(node != None): 
                print(node.key, end=" ") 
                node = node.forward[lvl] 
            print("") 
  
# Driver to test above code 
def main(): 
    lst = SkipList(3, 0.5) 
    lst.insertElement(3) 
    lst.insertElement(6) 
    lst.insertElement(7) 
    lst.insertElement(9) 
    lst.insertElement(12) 
    lst.insertElement(19) 
    lst.insertElement(17) 
    lst.insertElement(26) 
    lst.insertElement(21) 
    lst.insertElement(25) 
    lst.displayList() 
  
main() 
