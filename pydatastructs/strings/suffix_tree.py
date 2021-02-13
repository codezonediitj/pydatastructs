from pydatastructs.utils.misc_util import SuffixNode

__all__ = [
    'SuffixTree'
]

class SuffixTree(object):
    """
    Represents Suffix Tree.

    Examples
    ========

    >>> from pydatastructs.strings import SuffixTree as suffix
    >>> s = suffix('hello')
    >>> s.find('he')
    0
    >>> s.find_all('l')
    {2, 3}
    >>> s.find('f')
    -1
    >>> lt=["abeceda", "abecednik", "abeabecedabeabeced", "abecedaaaa", "aaabbbeeecceeeddaaaaabeceda"]
    >>> s1 = suffix(lt)
    >>> s1.longest_common_substring()
    'abeced'

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Suffix_tree
    .. [2] https://en.wikipedia.org/wiki/Generalized_suffix_tree
    """

    def __new__(cls, input=''):
        obj = object.__new__(cls)
        obj.root = SuffixNode()
        obj.root.depth = 0
        obj.root.idx = 0
        obj.root.parent = obj.root
        obj.root._add_suffix_link(obj.root)
        if not input == '':
            obj.build(input)
        return obj

    @classmethod
    def methods(cls):
        return ['__new__', 'lcs', 'find', 'find_all']

    def _check_input(self, input):
        """
        Check if the input is str ot list of str.
        """
        if isinstance(input, str):
            return 'str'
        elif isinstance(input, list):
            if all(isinstance(item, str) for item in input):
                return 'list'
        raise ValueError("String argument should be of type String or a list of strings")

    def build(self, x):
        """
        Builds the Suffix tree on the given input.

        Parameters
        ==========

        x: str or list of str

        Returns
        =======

        None
        """
        type = self._check_input(x)
        if type == 'str':
            x += next(self._terminal_symbols_generator())
            self._build(x)
        if type == 'list':
            self._build_generalized(x)

    def _build(self, x):
        """
        Builds suffix tree with string.
        """
        self.word = x
        self._build_McCreight(x)

    def _build_McCreight(self, x):
        u = self.root
        d = 0
        for i in range(len(x)):
            while u.depth == d and u._has_transition(x[d + i]):
                u = u._get_transition_link(x[d + i])
                d = d + 1
                while d < u.depth and x[u.idx + d] == x[i + d]:
                    d = d + 1
            if d < u.depth:
                u = self._create_node(x, u, d)
            self._create_leaf(x, i, u, d)
            if not u._get_suffix_link():
                self._compute_slink(x, u)
            u = u._get_suffix_link()
            d = d - 1
            if d < 0:
                d = 0

    def _create_node(self, x, u, d):
        """
        Creates node for the suffix tree
        with transition links.
        """
        i = u.idx
        p = u.parent
        v = SuffixNode(idx=i, depth=d)
        v._add_transition_link(u, x[i + d])
        u.parent = v
        p._add_transition_link(v, x[i + p.depth])
        v.parent = p
        return v

    def _create_leaf(self, x, i, u, d):
        """
        Creates the leaf node for the
        suffix tree.
        """
        w = SuffixNode()
        w.idx = i
        w.depth = len(x) - i
        u._add_transition_link(w, x[i + d])
        w.parent = u
        return w

    def _compute_slink(self, x, u):
        d = u.depth
        v = u.parent._get_suffix_link()
        while v.depth < d - 1:
            v = v._get_transition_link(x[u.idx + v.depth + 1])
        if v.depth > d - 1:
            v = self._create_node(x, v, d - 1)
        u._add_suffix_link(v)

    def _build_generalized(self, xs):
        """
        Builds the generalized suffix tree with list
        of string.
        """
        terminal_gen = self._terminal_symbols_generator()
        _xs = ''.join([x + next(terminal_gen) for x in xs])
        self.word = _xs
        self._generalized_word_starts(xs)
        self._build(_xs)
        self.root._traverse(self._label_generalized)

    def _label_generalized(self, node):
        """
        Helper method that labels the nodes of GST with
        indexes of strings found in their descendants.
        """
        if node.is_leaf():
            x = {self._get_word_start_index(node.idx)}
        else:
            x = {n for ns in node.transition_links.values() for n in ns.generalized_idxs}
        node.generalized_idxs = x

    def _get_word_start_index(self, idx):
        """
        Helper method that returns the index of the
        string based on node's starting index.
        """
        i = 0
        for _idx in self.word_starts[1:]:
            if idx < _idx:
                return i
            else:
                i += 1
        return i

    def longest_common_substring(self, stringIdxs = -1):
        """
        Finds the Largest Common Substring of Strings provided in stringIdxs.
        If stringIdxs is not provided, the LCS of all strings is returned.

        Parameters
        ==========

        stringIdxs: int or list of int

        Returns
        =======

        Longest Common Substring
        """
        if stringIdxs == -1 or not isinstance(stringIdxs, list):
            stringIdxs = set(range(len(self.word_starts)))
        else:
            stringIdxs = set(stringIdxs)
        deepestNode = self._find_lcs(self.root, stringIdxs)
        start = deepestNode.idx
        end = deepestNode.idx + deepestNode.depth
        return self.word[start:end]

    def _find_lcs(self, node, stringIdxs):
        """
        Helper method for longest common substring
        of the labelled Generalized suffix tree.
        """
        nodes = [self._find_lcs(n, stringIdxs)
                 for n in node.transition_links.values()
                 if n.generalized_idxs.issuperset(stringIdxs)]
        if nodes == []:
            return node
        deepestNode = max(nodes, key=lambda n: n.depth)
        return deepestNode

    def _generalized_word_starts(self, xs):
        """
        Helper method fidning the starting indexes
        of strings in Generalized suffix tree.
        """
        self.word_starts = []
        i = 0
        for n in range(len(xs)):
            self.word_starts.append(i)
            i += len(xs[n]) + 1

    def find(self, y):
        """
        Finds the starting position of the substring y in the string used for
        building the Suffix tree.

        Parameters
        ==========

        y: str

        Returns
        =======

        Index of the starting position of string y in the string used for building the Suffix tree
        -1 if y is not a substring.
        """
        node = self.root
        while True:
            edge = self._edge_label(node, node.parent)
            if edge.startswith(y):
                return node.idx

            i = 0
            while (i < len(edge) and edge[i] == y[0]):
                y = y[1:]
                i += 1

            if i != 0:
                if i == len(edge) and y != '':
                    pass
                else:
                    return -1

            node = node._get_transition_link(y[0])
            if not node:
                return -1

    def find_all(self, y):
        """
        Finds the starting position of the substring y in the string used for
        building the Suffix tree.

        Parameters
        ==========

        y: str

        Returns
        =======

        Set of Index of the starting positions of string y in the string used for building the Suffix tree
        {} if y is not a substring.
        """
        node = self.root
        while True:
            edge = self._edge_label(node, node.parent)
            if edge.startswith(y):
                break
            i = 0
            while (i < len(edge) and edge[i] == y[0]):
                y = y[1:]
                i += 1
            if i != 0:
                if i == len(edge) and y != '':
                    pass
                else:
                    return {}
            node = node._get_transition_link(y[0])
            if not node:
                return {}

        leaves = node._get_leaves()
        return {n.idx for n in leaves}

    def _edge_label(self, node, parent):
        """
        Helper method returns the edge label
        between a node and it's parent.
        """
        return self.word[node.idx + parent.depth: node.idx + node.depth]

    def _terminal_symbols_generator(self):
        """
        Generator of unique terminal symbols used for building the Generalized Suffix Tree.
        Unicode Private Use Area is used to ensure that terminal symbols are not part
        of the input string.
        """
        unicode = list(list(range(0xE000, 0xF8FF+1)) + list(range(0xF0000, 0xFFFFD+1)) + list(range(0x100000, 0x10FFFD+1)))
        for i in unicode:
            yield (chr(i))
        raise ValueError("To many input strings.")
