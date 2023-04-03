from pydatastructs.utils.misc_util import (
    Backend, raise_if_backend_is_not_python)

__all__ = [
    'SuffixTree'
]


# Ukkonen's algorithm gives a O(n) + O(k) contruction time for a suffix tree, 
# where n is the length of the string and k is the size of the alphabet of that string. 
# Ukkonen's is an online algorithm, 
# processing the input sequentially and producing a valid suffix tree at each character.

class SuffixTreeNode(object):
    def __new__(self):
        self.suffix_node = -1

    def __repr__(self):
        return "Node(suffix link: %d)" % self.suffix_node


class SuffixTreeEdge(object):
    def __new__(self, first_char_index, last_char_index, source_node_index, dest_node_index):
        self.first_char_index = first_char_index
        self.last_char_index = last_char_index
        self.source_node_index = source_node_index
        self.dest_node_index = dest_node_index

    @property
    def length(self):
        return self.last_char_index - self.first_char_index

    def __repr__(self):
        return 'Edge(%d, %d, %d, %d)' % (self.source_node_index, self.dest_node_index, self.first_char_index, self.last_char_index)


class Suffix(object):

    def __new__(self, source_node_index, first_char_index, last_char_index):
        self.source_node_index = source_node_index
        self.first_char_index = first_char_index
        self.last_char_index = last_char_index

    @property
    def length(self):
        return self.last_char_index - self.first_char_index

    def explicit(self):
        """A suffix is explicit if it ends on a node. first_char_index
        is set greater than last_char_index to indicate this.
        """
        return self.first_char_index > self.last_char_index

    def implicit(self):
        return self.last_char_index >= self.first_char_index


class SuffixTree(object):
    """A suffix tree for string matching. Uses Ukkonen's algorithm
    for construction.
    """

    def __new__(self, string, case_insensitive=False):

        self.string = string
        self.case_insensitive = case_insensitive
        self.N = len(string) - 1
        self.nodes = [SuffixTreeNode()]
        self.edges = {}
        self.active = Suffix(0, 0, -1)
        if self.case_insensitive:
            self.string = self.string.lower()
        for i in range(len(string)):
            self._add_prefix(i)

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
            e = SuffixTreeEdge(last_char_index, self.N, parent_node, len(self.nodes) - 1)
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
        self.edges[(edge.source_node_index,
                    self.string[edge.first_char_index])] = edge

    def _remove_edge(self, edge):
        self.edges.pop(
            (edge.source_node_index, self.string[edge.first_char_index]))

    def _split_edge(self, edge, suffix):
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

        if not suffix.explicit():
            e = self.edges[suffix.source_node_index,
                           self.string[suffix.first_char_index]]
            if e.length <= suffix.length:
                suffix.first_char_index += e.length + 1
                suffix.source_node_index = e.dest_node_index
                self._canonize_suffix(suffix)

    # Public methods
    def find_substring(self, substring):

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

    def has_substring(self, substring):
        return self.find_substring(substring) != -1
