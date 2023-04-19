from pydatastructs.utils.misc_util import (
    SuffixTreeNode, SuffixTreeEdge, Suffix, Backend, raise_if_backend_is_not_python)

__all__ = [
    'SuffixTree'
]


class SuffixTree(object):
    """
    Represents a suffix tree.

    Parameters
    ==========
    string
        Required, it represents the sequence of
        characters around which the construction
        of the suffix tree takes place

    case_insensitive
        Optional, through this parameter it's specified
        if the suffix tree should consider the case of
        the given characters; otherwise set to False,
        meaning that 'A' is different from 'a'

    References
    ==========
    .. [1] https://en.wikipedia.org/wiki/Suffix_tree
    """
    @classmethod
    def methods(cls):
        return ['__new__', '__init__', '__repr__',
                'find', 'has']

    def __new__(cls, string="", case_insensitive=False, **kwargs):
        obj = object.__new__(cls)
        obj.string = string
        obj.case_insensitive = case_insensitive
        obj.N = len(string) - 1
        obj.nodes = [SuffixTreeNode()]
        obj.edges = {}
        obj.active = Suffix(0, 0, -1)
        if obj.case_insensitive:
            obj.string = obj.string.lower()
        for i in range(len(string)):
            obj._add_prefix(i)
        return obj
    
    def __init__(self, string="", case_insensitive=False):
        self = self.__new__(SuffixTree, string, case_insensitive)

    def __repr__(self):
        curr_index = self.N
        s = "\tStart \tEnd \tSuf \tFirst \tLast \tString\n"
        values = list(self.edges.values())
        values.sort(key=lambda x: x.source_node_index)
        for edge in values:
            if edge.source_node_index == -1:
                continue
            s += "\t%s \t%s \t%s \t%s \t%s \t" % (edge.source_node_index, edge.dest_node_index,
                                                  self.nodes[edge.dest_node_index].suffix_node, edge.first_char_index, edge.last_char_index)

            top = min(curr_index, edge.last_char_index)
            s += self.string[edge.first_char_index:top + 1] + "\n"
        return s

    def _add_prefix(self, last_char_index):
        """
        This method adds a prefix to the suffix tree using Ukkonen's algorithm.
        It starts from the active node and iteratively inserts the prefix into the tree.

        Parameters
        ==========
        last_char_index
            The index of the last character to be added to the tree.

        Returns
        =======
        None
        """
        last_parent_node = -1
        while True:
            parent_node = self.active.source_node_index
            if self.active.explicit():
                if (self.active.source_node_index, self.string[last_char_index]) in self.edges:
                    # prefix is already in tree
                    break
            else:
                e = self.edges[self.active.source_node_index,
                               self.string[self.active.first_char_index]]
                if self.string[e.first_char_index + self.active.length + 1] == self.string[last_char_index]:
                    # prefix is already in tree
                    break
                parent_node = self._split_edge(e, self.active)

            self.nodes.append(SuffixTreeNode())
            e = SuffixTreeEdge(last_char_index, self.N,
                               parent_node, len(self.nodes) - 1)
            self._insert_edge(e)

            if last_parent_node > 0:
                self.nodes[last_parent_node].suffix_node = parent_node
            last_parent_node = parent_node

            if self.active.source_node_index == 0:
                self.active.first_char_index += 1
            else:
                self.active.source_node_index = self.nodes[self.active.source_node_index].suffix_node
            self._canonize_suffix(self.active)
        if last_parent_node > 0:
            self.nodes[last_parent_node].suffix_node = parent_node
        self.active.last_char_index += 1
        self._canonize_suffix(self.active)

    def _insert_edge(self, edge):
        """
        Inserts a new edge into the suffix tree using the Ukkonen's
        algorithm.

        Parameters
        ==========
        edge
            The Edge object to be inserted.

        Returns
        =======
        None
        """
        self.edges[(edge.source_node_index,
                    self.string[edge.first_char_index])] = edge

    def _remove_edge(self, edge):
        """
        Removes the edge passed as parameter from the suffix tree using
        the Ukkonen algorithm.

        Parameters
        ==========
        edge
            The edge to be removed.

        Returns
        =======
        None
        """
        self.edges.pop(
            (edge.source_node_index, self.string[edge.first_char_index]))

    def _split_edge(self, edge, suffix):
        """
        Inserts a new node and creates a new edge by splitting 
        an existing edge in the suffix tree using Ukkonen algorithm.

        Parameters
        ==========
        edge
            The edge to be split.
        suffix
            The suffix to be inserted.

        Returns
        =======
        None
        """
        self.nodes.append(SuffixTreeNode())
        e = SuffixTreeEdge(edge.first_char_index, edge.first_char_index + suffix.length, suffix.source_node_index,
                           len(self.nodes) - 1)
        self._remove_edge(edge)
        self._insert_edge(e)
        # need to add node for each edge
        self.nodes[e.dest_node_index].suffix_node = suffix.source_node_index
        edge.first_char_index += suffix.length + 1
        edge.source_node_index = e.dest_node_index
        self._insert_edge(edge)
        return e.dest_node_index

    def _canonize_suffix(self, suffix):
        """
        Canonize the given suffix using the iterative Ukkonen's algorithm
        in the suffix tree.

        Parameters
        ==========
        suffix
            The suffix to be canonized.

        Returns
        =======
        None
        """
        if not suffix.explicit():
            e = self.edges[suffix.source_node_index,
                           self.string[suffix.first_char_index]]
            if e.length <= suffix.length:
                suffix.first_char_index += e.length + 1
                suffix.source_node_index = e.dest_node_index
                self._canonize_suffix(suffix)

    # Public methods
    def find(self, substring):
        """
        Searches for the given substring in the suffix tree using Ukkonen's algorithm.

        Parameters
        ==========
        substring
            The substring to search for.

        Returns
        =======
        None
        """
        if not substring:
            return -1
        if self.case_insensitive:
            substring = substring.lower()
        curr_node = 0
        i = 0
        while i < len(substring):
            edge = self.edges.get((curr_node, substring[i]))
            if not edge:
                return -1
            ln = min(edge.length + 1, len(substring) - i)
            if substring[i:i + ln] != self.string[edge.first_char_index:edge.first_char_index + ln]:
                return -1
            i += edge.length + 1
            curr_node = edge.dest_node_index
        return edge.first_char_index - len(substring) + ln

    def has(self, substring):
        """
        Checks if the given substring is present in the suffix tree using the
        find() method and returns True if present, False otherwise.

        Parameters
        ==========
        substring
            The substring to be searched for in the suffix tree.

        Returns
        =======
        bool
            True if the substring is present in the suffix tree, False otherwise
        """
        return self.find(substring) != -1
