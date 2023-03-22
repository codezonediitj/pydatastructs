from pydatastructs.utils.misc_util import (
    TrieNode, Backend,
    raise_if_backend_is_not_python)
from collections import deque
import copy

__all__ = [
    'Trie'
]

Stack = Queue = deque

class Trie(object):
    """
    Represents the trie data structure for storing strings.

    Parameters
    ==========

    backend: pydatastructs.Backend
        The backend to be used.
        Optional, by default, the best available
        backend is used.

    Examples
    ========

    >>> from pydatastructs import Trie
    >>> trie = Trie()
    >>> trie.insert("a")
    >>> trie.insert("aa")
    >>> trie.strings_with_prefix("a")
    ['a', 'aa']
    >>> trie.is_present("aa")
    True
    >>> trie.delete("aa")
    True
    >>> trie.is_present("aa")
    False

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Trie
    """

    __slots__ = ['root']

    @classmethod
    def methods(cls):
        return ['__new__', 'insert', 'is_present', 'delete',
                'strings_with_prefix']

    def __new__(cls, **kwargs):
        raise_if_backend_is_not_python(
            cls, kwargs.get('backend', Backend.PYTHON))
        obj = object.__new__(cls)
        obj.root = TrieNode()
        return obj

    def insert(self, string: str) -> None:
        """
        Inserts the given string into the trie.

        Parameters
        ==========

        string: str

        Returns
        =======

        None
        """
        walk = self.root
        for char in string:
            if walk.get_child(char) is None:
                newNode = TrieNode(char)
                walk.add_child(newNode)
                walk = newNode
            else:
                walk = walk.get_child(char)
        walk.is_terminal = True

    def is_present(self, string: str) -> bool:
        """
        Checks if the given string is present as a prefix in the trie.

        Parameters
        ==========

        string: str

        Returns
        =======

        True if the given string is present as a prefix;
        False in all other cases.
        """
        walk = self.root
        for char in string:
            if walk.get_child(char) is None:
                return False
            walk = walk.get_child(char)
        return True

    def is_inserted(self, string: str) -> bool:
        """
        Checks if the given string was inserted in the trie.

        Parameters
        ==========

        string: str

        Returns
        =======

        True if the given string was inserted in trie;
        False in all other cases.
        """
        walk = self.root
        for char in string:
            if walk.get_child(char) is None:
                return False
            walk = walk.get_child(char)
        return walk.is_terminal

    def delete(self, string: str) -> bool:
        """
        Deletes the given string from the trie.

        Parameters
        ==========

        string: str

        Returns
        =======

        True if successfully deleted;
        None if the string is not present in the trie.
        """
        path = []
        walk = self.root
        size = len(string)
        for i in range(size):
            char = string[i]
            path.append(walk)
            if walk.get_child(char) is None:
                return None
            walk = walk.get_child(char)
        path.append(walk)
        i = len(path) - 1
        path[i].is_terminal = False
        while not path[i]._children and i >= 1:
            path[i-1].remove_child(path[i].char)
            i -= 1
            if path[i].is_terminal:
                return True
        return True

    def strings_with_prefix(self, string: str) -> list:
        """
        Generates a list of all strings with the given prefix.

        Parameters
        ==========

        string: str

        Returns
        =======

        strings: list
            The list of strings with the given prefix.
        """

        def _collect(prefix: str, node: TrieNode, strings: list) -> str:
            TrieNode_stack = Stack()
            TrieNode_stack.append((node, prefix))
            while TrieNode_stack:
                walk, curr_prefix = TrieNode_stack.pop()
                if walk.is_terminal:
                    strings.append(curr_prefix + walk.char)
                for child in walk._children:
                    TrieNode_stack.append((walk.get_child(child), curr_prefix + walk.char))

        strings = []
        prefix = ""
        walk = self.root
        for char in string:
            walk = walk.get_child(char)
            if walk is None:
                return strings
            prefix += char
        if walk.is_terminal:
            strings.append(walk.char)
        for child in walk._children:
            _collect(prefix, walk.get_child(child), strings)
        return strings
