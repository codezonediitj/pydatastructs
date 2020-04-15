'''
        Represents a trie data structure.

        Parameters
        ==========
        dtype: type
            A valid object type.
        N: number of keys in trie
        K: world inserting or searching 
        alphabet_size: size of alphabet *26

        Raises
        ======
        IndexError
            Index goes out of boundaries
        ValueError
            When there's no dimensions or the dimension size is 0
        TypeError
            An argument is not what expected

        Examples
        ========
        >>> from pydatastructs import trie_structure as 
        >>> key = ["hi","bye"]
        >>> output = ["Not present in trie", 
              "Present in trie"] 
        >>> new = Trie()
        >>> for key in keys: 
               new.insert(key)
        >>> output[new.search("bye")]
        "Present in trie"
        >>> output[new.search("the")]
        "Not present in trie"

        References
        ==========
        .. [1] https://www.geeksforgeeks.org/trie-insert-and-search/
        '''

#Init node class
class TrieNode: 
      
    def __init__(self): 
        self.children = [None]*26 #26 because we are taking the alphabet_size 
  
        # isEndOfWord is True if node represent the end of the word 
        self.isEndOfWord = False

#Init class trie 
class Trie: 
      
    def __init__(self): 
        self.root = self.getNode() 
  
    def getNode(self): 
      
        return TrieNode()  #Returns new trie node (initialized to NULLs) 
  
    def _charToIndex(self,ch): 
        '''
        Notes to know about char to Index func:
        Converts key current character into index 
        Using only 'a' through 'z' and lower case 
        Ord() definition: Given a string of length one, return an integer representing the Unicode code point of the character when the argument is a unicode object, or the value of the byte when the argument is an 8-bit string.
        '''
        return ord(ch)-ord('a') 
    
    def insert(self,key): 
        '''
        Notes to know about insertion in trie structure:
        Every character of input key is inserted as an individual trie node.
        The children is an array of pointers to next level trie nodes.
        Key refers to the world that you are inserting or searching in the trie

        Insert and search costs O(k) where k is length of key.
        The memory requirements of trie is O(alphabet_size*k*N) where N is number of keys in trie.

          
        If not present, inserts key into trie 
        If the key is prefix of trie node, just marks leaf node 
        ''' 
        pC = self.root 
        length = len(key) 
        for level in range(length): 
            index = self._charToIndex(key[level])  #charToIndex function above
  
            # if character not present:
            if not pC.children[index]: 
                pC.children[index] = self.getNode() 
            pC = pC.children[index] 
  
        #marking last node as leaf:
        pC.isEndOfWord = True #isEndOfWord is True if node represent the end of the word
    
    def search(self, key): 
        '''
        Notes to know about searching in trie structure:
        While searching we only compare the characters and move down.
        Search key in the trie .
        Returning true if key presents in trie, else false. 
        The search can end because of end of a string, if the value field of last node is non-zero then the key exists in trie.
        '''
        pC = self.root 
        length = len(key) 
        for level in range(length): 
            index = self._charToIndex(key[level]) #charToIndex function above
            if not pC.children[index]: 
                return False
            pC = pC.children[index] 
  
        return pC != None and pC.isEndOfWord #and is a boolean expression  | isEndofWord: True if node represent the end of the word
    
    def delete(self,key):
        pC=self.root

        if self.search(key):
            for c in key:
                index = self._charToIndex(c)
                pC = pC.children[index]
            
            pC.isEndOfWord = False





        
   
def main(): 
  
    # Input keys with charToIndex rule of a-z in lowercase
    keys = ["hi","pydatastructs","this","is","a", 
            "try","trie"] 
    output = ["Not present in trie", 
              "Present in trie"] 
  
    # Trie object 
    t = Trie() #new class Trie | Object
  
    # Construct trie, inserting keys
    for key in keys: 
        t.insert(key) 
  
    # Search for different keys 
    print("{} ---- {}".format("trie",output[t.search("trie")])) 
    print("{} ---- {}".format("bye",output[t.search("bye")])) 
    print("{} ---- {}".format("no",output[t.search("no")])) 
    print("{} ---- {}".format("pydatastructs",output[t.search("pydatastructs")])) 
    
    #delete function
    print("{} ---- {}".format("try",output[t.search("try")]))
    t.delete("try")
    print("{} ---- {}".format("try",output[t.search("try")]))


  
if __name__ == '__main__': 
    main() 
  
  