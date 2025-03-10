"""
Implementation of Trie (Prefix Tree) data structure.
"""

__all__ = [
    'Trie'
]

class TrieNode:
    """
    Represents a node in the Trie.
    """
    __slots__ = ['children', 'is_end_of_word']

    def __init__(self):
        """
        Initializes a TrieNode.
        """
        self.children = {}
        self.is_end_of_word = False

class Trie:
    """
    Represents a Trie (Prefix Tree) data structure.
    
    Examples
    ========
    
    >>> from pydatastructs.trees.trie import Trie
    >>> trie = Trie()
    >>> trie.insert("apple")
    >>> trie.search("apple")
    True
    >>> trie.search("app")
    False
    >>> trie.starts_with("app")
    True
    >>> trie.insert("app")
    >>> trie.search("app")
    True
    >>> trie.delete("apple")
    True
    >>> trie.search("apple")
    False
    >>> trie.search("app")
    True
    """
    __slots__ = ['root']

    def __init__(self):
        """
        Initializes an empty Trie.
        """
        self.root = TrieNode()

    def insert(self, word):
        """
        Inserts a word into the trie.
        
        Parameters
        ==========
        
        word: str
            The word to insert
            
        Returns
        =======
        
        None
        """
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, word):
        """
        Returns True if the word is in the trie.
        
        Parameters
        ==========
        
        word: str
            The word to search for
            
        Returns
        =======
        
        bool
            True if the word is in the trie, False otherwise
        """
        node = self._get_node(word)
        return node is not None and node.is_end_of_word

    def starts_with(self, prefix):
        """
        Returns True if there is any word in the trie
        that starts with the given prefix.
        
        Parameters
        ==========
        
        prefix: str
            The prefix to check
            
        Returns
        =======
        
        bool
            True if there is any word with the given prefix,
            False otherwise
        """
        return self._get_node(prefix) is not None

    def delete(self, word):
        """
        Deletes a word from the trie if it exists.
        
        Parameters
        ==========
        
        word: str
            The word to delete
            
        Returns
        =======
        
        bool
            True if the word was deleted, False if it wasn't in the trie
        """
        def _delete_helper(node, word, depth=0):
            # If we've reached the end of the word
            if depth == len(word):
                # If the word exists in the trie
                if node.is_end_of_word:
                    node.is_end_of_word = False
                    # Return True if this node can be deleted
                    # (has no children and is not end of another word)
                    return len(node.children) == 0
                return False
            
            char = word[depth]
            if char not in node.children:
                return False
            
            should_delete_child = _delete_helper(node.children[char], word, depth + 1)
            
            # If we should delete the child
            if should_delete_child:
                del node.children[char]
                # Return True if this node can be deleted
                # (has no children and is not end of another word)
                return len(node.children) == 0 and not node.is_end_of_word
            
            return False
        
        if not word:
            return False
        
        return True if _delete_helper(self.root, word) else self.search(word)

    def _get_node(self, prefix):
        """
        Returns the node at the end of the prefix, or None if not found.
        
        Parameters
        ==========
        
        prefix: str
            The prefix to find
            
        Returns
        =======
        
        TrieNode or None
            The node at the end of the prefix, or None if the prefix doesn't exist
        """
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node