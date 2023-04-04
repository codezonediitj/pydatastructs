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

if __name__ == '__main__':
    test_suffix_tree()
