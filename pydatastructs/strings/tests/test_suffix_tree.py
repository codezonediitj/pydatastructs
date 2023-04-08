from pydatastructs.strings.suffix_tree import SuffixTree

def test_suffix_tree():
    """Some functional tests.
    """

    # test_empty_string(self):
    st = SuffixTree('')
    assert (st.find_substring('not there') == -1)
    assert (st.find_substring('') == -1)
    assert (st.has_substring('not there') is False)
    assert (st.has_substring('') is False)

    # test_repeated_string(self):
    st = SuffixTree("aaa")
    assert (st.find_substring('a') == 0)
    assert (st.find_substring('aa') == 0)
    assert (st.find_substring('aaa') == 0)
    assert (st.find_substring('b') == -1)
    assert (st.has_substring('a') is True)
    assert (st.has_substring('aa') is True)
    assert (st.has_substring('aaa') is True)

    assert (st.has_substring('aaaa') is False)
    assert (st.has_substring('b') is False)
    # case sensitive by default
    assert (st.has_substring('A') is False)
    assert (st.find_substring('x') == -1)

    # test with case insensitve
    st = SuffixTree("aaa", True)
    assert (st.find_substring('a') == 0)
    assert (st.find_substring('aa') == 0)
    assert (st.find_substring('aaa') == 0)
    assert (st.find_substring('b') == -1)
    assert (st.has_substring('a') is True)
    assert (st.has_substring('aa') is True)
    assert (st.has_substring('aaa') is True)

    assert (st.has_substring('aaaa') is False)
    assert (st.has_substring('b') is False)
    # case sensitive set manually
    assert (st.has_substring('A') is True)
    assert (st.find_substring('x') == -1)

    # test repr method
    assert (repr(st) == str("\tStart \tEnd \tSuf \tFirst \tLast \tString\n\t0 \t1 \t-1 \t0 \t2 \taaa\n"))

    # check methods function
    assert (st.methods() == ['__new__', '__init__', '__repr__', 'find_substring', 'has_substring'])

def test_suffix_tree2():
    f = open("./pydatastructs/strings/tests/long_string.txt", encoding = "iso-8859-1")
    st = SuffixTree(f.read())
    assert (st.find_substring('Ukkonen') == 1498)
    assert (st.find_substring('Optimal') == 11131)
    assert (st.has_substring('ukkonen') is False)
    f.close()

if __name__ == '__main__':
    test_suffix_tree()
