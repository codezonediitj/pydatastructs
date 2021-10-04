from pydatastructs import SuffixTree
from pydatastructs.utils.raises_util import raises
import random, string

def test_suffixtree():
    """
    References
    ==========
    .. https://www.cise.ufl.edu/~sahni/dsaaj/enrich/c16/suffix.htm

    """
    s = SuffixTree("HelloworldHe")
    assert s.find("Hel") == 0
    assert s.find_all("He") == {0, 10}
    assert s.find("Win") == -1
    assert s.find_all("go") == {}
    assert raises(AttributeError, lambda: s.longest_common_substring())

    f = ['integer', 'inteinteger', 'integralerint', 'iaingerntier', 'regetnerireg', 'reger']
    s = SuffixTree(f)
    assert s.longest_common_substring() == 'er'
    f = ['integer', 'inteinteger', 'integralerint', 'iainegerntier', 'regetnerireg', 'reger']
    s = SuffixTree(f)
    assert s.longest_common_substring(7) == 'eg'

    assert raises(ValueError, lambda: SuffixTree(123))
    res = (100, 1, 0)
    assert raises(ValueError, lambda: SuffixTree(res))
