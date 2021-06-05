from pydatastructs.linear_data_structures.arrays import (
    OneDimensionalArray)

__all__ = [
    'find_string'
]

def find_string(text: str, pattern: str, algorithm: str) -> bool:
    """API of finding occurrence of a pattern string within another string or body of text.

    Parameters
    ----------
    text: str
        A text, set of characters can include alphabets, numbers , special characters and blank spaces
    pattern: str
        A text, set of characters can include alphabets, numbers , special characters and blank spaces
    algorithm: str
        A valid algorithm name

    Returns
    -------
    bool
        True if pattern occurs in the string, else False

    Examples
    --------
    >>> from pydatastructs.strings.string_matching_algorithms import find_string
    >>> find_string("aefoaefcdaefcdaed", "aefcdaed", algorithm = "kmp")
    True
    >>> find_string("aefoaefcdaefcdaed", "aefcdaedz", algorithm = "kmp")
    False

    """
    return eval(algorithm + "('" + text + "','" + pattern + "')")


def kmp(string: str, substring: str) -> bool:
    """Determine whether the substring appears somewhere in the string using Knuth–Morris–Pratt algorithm

    Parameters
    ----------
    string: str
        A text, set of characters
    substring: str
        A pattern/substring that is searched for in the string

    Returns
    -------
    bool
        Whether substring exists in the string or not

    Examples
    --------
    >>> from pydatastructs.strings.string_matching_algorithms import kmp
    >>> kmp("aefoaefcdaefcdaed", "aefcdaed")
    True
    >>> kmp("aefoaefcdaefcdaed", "aefcdaedz")
    False

    References
    -------
    .. [1] https://www.inf.hs-flensburg.de/lang/algorithmen/pattern/kmpen.htm
    .. [2] https://towardsdatascience.com/pattern-search-with-the-knuth-morris-pratt-kmp-algorithm-8562407dba5b
    .. [3] https://iopscience.iop.org/article/10.1088/1742-6596/1345/4/042005/pdf

    """
    patternsInSubString = _buildPattern(substring)
    return _doMatch(string, substring, patternsInSubString)


def _buildPattern(substring: str) -> OneDimensionalArray:
    """Check for patterns existing in the substring

    Parameters
    ----------
    substring: str
        A text, set of characters

    Returns
    -------
    patterns: OneDimensionalArray
        Returns an array of indicies. For a given index if value > -1
        represents that the suffix found at the index, is also the prefix
        at the value index. If value is -1, then there is no prefix that is also
        a suffix.

    """
    j = 0
    i = 1
    patterns = OneDimensionalArray(int, len(substring))
    patterns.fill(-1)
    while i < len(substring):
        if substring[i] is substring[j]:
            # A prefix that is also a suffix
            patterns[i] = j
            i += 1
            j += 1
        elif j > 0:
            # Check the previous existing pattern
            j = patterns[j - 1] + 1
        else:
            i += 1
    return patterns


def _doMatch(string: str, substring: str, patterns: OneDimensionalArray) -> bool:
    """Check if the string exists in the substring

    Parameters
    ----------
    string: str
        A text, set of characters
    substring: str
        A pattern/substring that is searched for in the string
    patterns: OneDimensionalArray
        An array of integers, each value < len(patterns)

    Returns
    -------
    bool
        Whether substring exists in the string or not

    """
    i = 0
    j = 0
    while i < len(string):
        if string[i] is substring[j]:
            i += 1
            j += 1
        elif j > 0:
            j = patterns[j - 1] + 1
        else:
            i += 1
        if j is len(substring):
            return True
    return False
