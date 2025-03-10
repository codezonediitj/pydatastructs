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
                'strings_with_prefix', 'count_words', 'longest_common_prefix',
                'autocomplete', 'bulk_insert', 'clear', 'is_empty',
                'all_words', 'shortest_unique_prefix', 'starts_with',
                'longest_word']

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

        def _collect(node: TrieNode, prefix: str, strings: list):
            if node.is_terminal:
                strings.append(prefix)
            for child in node._children:
                _collect(node.get_child(child), prefix + child, strings)

        strings = []
        walk = self.root
        for char in string:
            if walk.get_child(char) is None:
                return strings
            walk = walk.get_child(char)
        _collect(walk, string, strings)
        return strings

    def count_words(self) -> int:
        """
        Returns the total number of words inserted into the trie.

        Returns
        =======

        count: int
            The total number of words in the trie.
        """
        def _count(node: TrieNode) -> int:
            count = 0
            if node.is_terminal:
                count += 1
            for child in node._children:
                count += _count(node.get_child(child))
            return count

        return _count(self.root)

    def longest_common_prefix(self) -> str:
        """
        Finds the longest common prefix among all the words in the trie.

        Returns
        =======

        prefix: str
            The longest common prefix.
        """
        prefix = ""
        walk = self.root
        while len(walk._children) == 1 and not walk.is_terminal:
            char = next(iter(walk._children))
            prefix += char
            walk = walk.get_child(char)
        return prefix

    def autocomplete(self, prefix: str) -> list:
        """
        Provides autocomplete suggestions based on the given prefix.

        Parameters
        ==========

        prefix: str

        Returns
        =======

        suggestions: list
            A list of autocomplete suggestions.
        """
        return self.strings_with_prefix(prefix)

    def bulk_insert(self, words: list) -> None:
        """
        Inserts multiple words into the trie.

        Parameters
        ==========

        words: list
            A list of words to be inserted.

        Returns
        =======

        None
        """
        for word in words:
            self.insert(word)

    def clear(self) -> None:
        """
        Clears the trie, removing all words.

        Returns
        =======

        None
        """
        self.root = TrieNode()

    def is_empty(self) -> bool:
        """
        Checks if the trie is empty.

        Returns
        =======

        bool
            True if the trie is empty, False otherwise.
        """
        return not self.root._children

    def all_words(self) -> list:
        """
        Retrieves all words stored in the trie.

        Returns
        =======

        words: list
            A list of all words in the trie.
        """
        return self.strings_with_prefix("")

    def shortest_unique_prefix(self) -> dict:
        """
        Finds the shortest unique prefix for each word in the trie.

        Returns
        =======
        prefixes: dict
            A dictionary where keys are words and values are their shortest unique prefixes.
        """
        def _find_prefix(node: TrieNode, prefix: str, prefixes: dict, word: str = ""):
            if node.is_terminal:
                prefixes[word] = prefix  # Store full word as key
            for child in node._children:
                new_word = word + child  # Build full word
                new_prefix = prefix + child
                if len(node._children) > 1 or node.is_terminal:
                    _find_prefix(node.get_child(child), new_prefix, prefixes, new_word)
                else:
                    _find_prefix(node.get_child(child), prefix, prefixes, new_word)

        prefixes = {}
        _find_prefix(self.root, "", prefixes)
        return prefixes


    def starts_with(self, prefix: str) -> bool:
        """
        Checks if any word in the trie starts with the given prefix.

        Parameters
        ==========

        prefix: str

        Returns
        =======

        bool
            True if any word starts with the prefix, False otherwise.
        """
        walk = self.root
        for char in prefix:
            if walk.get_child(char) is None:
                return False
            walk = walk.get_child(char)
        return True

    def longest_word(self) -> str:
        """
        Finds the longest word stored in the trie.

        Returns
        =======

        word: str
            The longest word in the trie.
        """
        def _longest(node: TrieNode, current_word: str, longest_word: str) -> str:
            if node.is_terminal and len(current_word) > len(longest_word):
                longest_word = current_word
            for child in node._children:
                longest_word = _longest(node.get_child(child), current_word + child, longest_word)
            return longest_word

        return _longest(self.root, "", "")