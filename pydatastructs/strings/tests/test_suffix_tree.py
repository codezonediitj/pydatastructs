from pydatastructs.strings.suffix_tree import SuffixTree
from pydatastructs.utils.misc_util import SuffixTreeNode, SuffixTreeEdge, Suffix


def test_suffix_tree():
    """Some functional tests.
    """

    # test_empty_string(self):
    st = SuffixTree('')
    assert (st.find('not there') == -1)
    assert (st.find('') == -1)
    assert (st.has('not there') is False)
    assert (st.has('') is False)

    # test_repeated_string(self):
    st = SuffixTree("aaa")
    assert (st.find('a') == 0)
    assert (st.find('aa') == 0)
    assert (st.find('aaa') == 0)
    assert (st.find('b') == -1)
    assert (st.has('a') is True)
    assert (st.has('aa') is True)
    assert (st.has('aaa') is True)

    assert (st.has('aaaa') is False)
    assert (st.has('b') is False)
    # case sensitive by default
    assert (st.has('A') is False)
    assert (st.find('x') == -1)

    # test with case insensitve
    st = SuffixTree("aaa", True)
    assert (st.find('a') == 0)
    assert (st.find('aa') == 0)
    assert (st.find('aaa') == 0)
    assert (st.find('b') == -1)
    assert (st.has('a') is True)
    assert (st.has('aa') is True)
    assert (st.has('aaa') is True)

    assert (st.has('aaaa') is False)
    assert (st.has('b') is False)
    # case sensitive set manually
    assert (st.has('A') is True)
    assert (st.find('x') == -1)

    # test repr method
    assert (repr(st) == str(
        "\tStart \tEnd \tSuf \tFirst \tLast \tString\n\t0 \t1 \t-1 \t0 \t2 \taaa\n"))

    # check methods function
    assert (st.methods() == ['__new__', '__init__',
            '__repr__', 'find', 'has'])


def test_suffix_tree2():
    f = open("./pydatastructs/strings/tests/long_string.txt",
             encoding="iso-8859-1")
    st = SuffixTree(f.read())
    assert (st.find('Ukkonen') == 1498)
    assert (st.find('Optimal') == 11131)
    assert (st.has('ukkonen') is False)
    f.close()


def test_suffix_tree3():
    # Test SuffixTreeNode
    node = SuffixTreeNode()
    assert isinstance(node, SuffixTreeNode)
    assert (node.suffix_node == -1)
    assert (repr(node) == "Node(suffix link: -1)")

    # Test SuffixTreeEdge
    edge = SuffixTreeEdge(0, 3, 1, 2)
    assert isinstance(edge, SuffixTreeEdge)
    assert (edge.first_char_index == 0)
    assert (edge.last_char_index == 3)
    assert (edge.source_node_index == 1)
    assert (edge.dest_node_index == 2)
    assert (edge.length == 3)
    assert (repr(edge) == "Edge(1, 2, 0, 3)")

    # Test Suffix implicit() method
    suffix = Suffix(1, 2, 3)
    assert isinstance(suffix, Suffix)
    assert (suffix.source_node_index == 1)
    assert (suffix.first_char_index == 2)
    assert (suffix.last_char_index == 3)
    assert (suffix.length == 1)
    assert (suffix.explicit() is False)
    assert (suffix.implicit() is True)


def test_suffix_tree4():
    edge = SuffixTreeEdge(0, 5, -1, 1)
    assert (edge.source_node_index == -1)
    edge = SuffixTreeEdge(0, 5, 0, 1)
    assert (edge.source_node_index == 0)
    edge = SuffixTreeEdge(0, 5, 1, 2)
    assert (edge.source_node_index == 1)
    # Create a SuffixTree instance
    string = "banana"
    suffix_tree = SuffixTree(string)

    # Add some edges to the suffix tree
    edge1 = SuffixTreeEdge(-1, 1, -1, 1)
    suffix_tree.edges[(0, "b")] = edge1

    # Test the if condition
    assert (edge1.source_node_index == -1)
    assert (repr(suffix_tree) ==
            "\tStart \tEnd \tSuf \tFirst \tLast \tString\n\t0 \t2 \t-1 \t1 \t5 \tanana\n\t0 \t3 \t-1 \t2 \t5 \tnana\n")


if __name__ == '__main__':
    test_suffix_tree()
    test_suffix_tree2()
    test_suffix_tree3()
    test_suffix_tree4()
