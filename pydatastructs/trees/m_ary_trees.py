from pydatastructs.utils import MAryTreeNode, TrieNode
from pydatastructs.linear_data_structures.arrays import ArrayForTrees

__all__ = [
    'MAryTree',
    'Trie'
]

class MAryTree(object):
    """
    Abstract m-ary tree.

    Parameters
    ==========

    root_data
        Optional, the root node of the binary tree.
        If not of type MAryTreeNode, it will consider
        root as data and a new root node will
        be created.
    key
        Required if tree is to be instantiated with
        root otherwise not needed.
    comp: lambda
        Optional, A lambda function which will be used
        for comparison of keys. Should return a
        bool value. By default it implements less
        than operator.
    is_order_statistic: bool
        Set it to True, if you want to use the
        order statistic features of the tree.
    max_children
        Optional, specifies the maximum number of children
        a node can have. Defaults to 2 in case nothing is
        specified.

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/M-ary_tree
    """

    __slots__ = ['root_idx', 'max_children', 'comparator', 'tree', 'size',
                 'is_order_statistic']


    def __new__(cls, key=None, root_data=None, comp=None,
                is_order_statistic=False, max_children=2):
        obj = object.__new__(cls)
        if key is None and root_data is not None:
            raise ValueError('Key required.')
        key = None if root_data is None else key
        root = MAryTreeNode(key, root_data)
        root.is_root = True
        obj.root_idx = 0
        obj.max_children = max_children
        obj.tree, obj.size = ArrayForTrees(MAryTreeNode, [root]), 1
        obj.comparator = lambda key1, key2: key1 < key2 \
                        if comp is None else comp
        obj.is_order_statistic = is_order_statistic
        return obj

    def insert(self, key, data=None):
        """
        Inserts data by the passed key using iterative
        algorithm.

        Parameters
        ==========

        key
            The key for comparison.
        data
            The data to be inserted.

        Returns
        =======

        None
        """
        raise NotImplementedError("This is an abstract method.")

    def delete(self, key, **kwargs):
        """
        Deletes the data with the passed key
        using iterative algorithm.

        Parameters
        ==========

        key
            The key of the node which is
            to be deleted.

        Returns
        =======

        True
            If the node is deleted successfully.
        None
            If the node to be deleted doesn't exists.

        Note
        ====

        The node is deleted means that the connection to that
        node are removed but the it is still in tree.
        """
        raise NotImplementedError("This is an abstract method.")

    def search(self, key, **kwargs):
        """
        Searches for the data in the binary search tree
        using iterative algorithm.

        Parameters
        ==========

        key
            The key for searching.
        parent: bool
            If true then returns index of the
            parent of the node with the passed
            key.
            By default, False

        Returns
        =======

        int
            If the node with the passed key is
            in the tree.
        tuple
            The index of the searched node and
            the index of the parent of that node.
        None
            In all other cases.
        """
        raise NotImplementedError("This is an abstract method.")

    def to_binary_tree(self):
        """
        Converts an m-ary tree to a binary tree.

        Returns
        =======

        TreeNode
            The root of the newly created binary tree.
        """
        raise NotImplementedError("This is an abstract method.")


    def __str__(self):
        to_be_printed = ['' for i in range(self.tree._last_pos_filled + 1)]
        for i in range(self.tree._last_pos_filled + 1):
            if self.tree[i] is not None:
                node = self.tree[i]
                to_be_printed[i] = (node.key, node.data)
                for j in node.children:
                    if j is not None:
                        to_be_printed[i].append(j)
        return str(to_be_printed)


class Trie:
    """
            Represents a trie data structure.

            Parameters
            ==========
            dtype: type
                A valid object type.
            N: number of keys in trie
            K: world inserting or searching
            alphabet_size: size of alphabet *26

            Examples
            ========
            >>> from pydatastructs import Trie
            >>> keys = ["hi","bye"]
            >>> new = Trie()
            >>> for key in keys:
            >>>     new.insert(key)
            >>> new.search("bye")
            "Present in trie"
            >>> new.search("the")
            False
            >>> new.search(bie)
            ["bye"]

            References
            ==========
            .. [1] https://www.geeksforgeeks.org/trie-insert-and-search/
            .. [2] https://gist.github.com/huseynlilkin/d512e7e57dce32cc7317754c3d9d9bce
    """

    def __init__(self):
        self.root = self.get_node()

    def get_node(self):
        return TrieNode()

    def insert(self, key):
        '''
        Notes to know about insertion in trie structure:
        Every character of input key is inserted as an individual trie node.
        The children is an array of pointers to next level trie nodes.
        Key refers to the word that you are inserting or searching in the trie

        Insert and search costs O(k) where k is length of key.
        The memory requirements of trie is O(k*N) where N is number of keys in trie.


        If not present, inserts key into trie
        If the key is prefix of trie node, just marks leaf node
        '''
        current_node = self.root

        for ch in key:
            if ch not in current_node.children:
                current_node.children[ch] = self.get_node()
                current_node.children[ch].ch = ch
            current_node = current_node.children[ch]

        # marking last node as leaf:
        current_node.is_end = True
    def get_words(self, node):
        if len(node.children) > 0:
            words = []
            if node.is_end:
                words.append(node.ch)
            for child in node.children:
                for word in self.get_words(node.children[child]):
                    words.append(node.ch + word)
            return words
        else:
            return [node.ch]

    def search(self, key):
        '''
        Notes to know about searching in trie structure:
        While searching we only compare the characters and move down.
        Search key in the trie .
        Returning true if key presents in trie, else false.
        The search can end because of end of a string, if the value field of last node is non-zero then the key exists in trie.
        '''
        current_node = self.root
        similar_min = 2
        prefix = ""
        for ch in key:
            if ch in current_node.children:
                similar_min -=1
                prefix = prefix + current_node.ch
                current_node = current_node.children[ch]
            elif similar_min <= 0:
                words = []
                for word in self.get_words(current_node):
                    words.append(prefix + word)
                return words
            else:
                return False
        if current_node.is_end:
            return True
        else:
            words = []
            for word in self.get_words(current_node):
                words.append(prefix + word)
            return words

    def delete(self, key):
        pC = self.root

        if self.search(key) == True:
            for c in key:
                pC = pC.children[c]
            pC.isEndOfWord = False
