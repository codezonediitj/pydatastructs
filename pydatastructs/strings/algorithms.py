from pydatastructs.linear_data_structures.arrays import (
    DynamicOneDimensionalArray, OneDimensionalArray)

__all__ = [
    'find'
]

def find(text, query, algorithm):
    """
    Finds occurrence of a query string within the text string.

    Parameters
    ==========

    text: str
        The string on which query is to be performed.
    query: str
        The string which is to be searched in the text.
    algorithm: str
        The algorithm which should be used for
        searching.
        Currently the following algorithms are
        supported,
        'kmp' -> Knuth-Morris-Pratt as given in [1].

    Returns
    =======

    DynamicOneDimensionalArray
        An array of starting positions of the portions
        in the text which match with the given query.

    Examples
    ========

    >>> from pydatastructs.strings.algorithms import find
    >>> text = "abcdefabcabe"
    >>> pos = find(text, "ab", algorithm="kmp")
    >>> str(pos)
    "['0', '6', '9']"
    >>> pos = find(text, "abc", algorithm="kmp")
    >>> str(pos)
    "['0', '6']"
    >>> pos = find(text, "abe", algorithm="kmp")
    >>> str(pos)
    "['9']"
    >>> pos = find(text, "abed", algorithm="kmp")
    >>> str(pos)
    '[]'

    References
    ==========

    .. [1] https://www.inf.hs-flensburg.de/lang/algorithmen/pattern/kmpen.htm
    """
    import pydatastructs.strings.algorithms as algorithms
    func = "_" + algorithm
    if not hasattr(algorithms, func):
        raise NotImplementedError(
        "Currently %s algoithm for searching strings "
        "inside a text isn't implemented yet."
        %(algorithm))
    return getattr(algorithms, func)(text, query)


def _knuth_morris_pratt(text, query):
    kmp_table = _build_kmp_table(query)
    return _do_match(text, query, kmp_table)

_kmp = _knuth_morris_pratt

def _build_kmp_table(query):
    pos, cnd = 1, 0
    kmp_table = OneDimensionalArray(int, len(query) + 1)

    kmp_table[0] = -1

    while pos < len(query):
        if query[pos] == query[cnd]:
            kmp_table[pos] = kmp_table[cnd]
        else:
            kmp_table[pos] = cnd
            while cnd >= 0 and query[pos] != query[cnd]:
                cnd = kmp_table[cnd]
        pos, cnd = pos + 1, cnd + 1
    kmp_table[pos] = cnd

    return kmp_table



def _do_match(string, query, kmp_table):
    j, k = 0, 0
    positions = DynamicOneDimensionalArray(int, 0)

    while j < len(string):
        if query[k] == string[j]:
            j = j + 1
            k = k + 1
            if k == len(query):
                positions.append(j - k)
                k = kmp_table[k]
        else:
            k = kmp_table[k]
            if k < 0:
                j = j + 1
                k = k + 1

    return positions
