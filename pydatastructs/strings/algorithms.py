from pydatastructs.linear_data_structures.arrays import (
    DynamicOneDimensionalArray, OneDimensionalArray)
from pydatastructs.utils.misc_util import (
    Backend, raise_if_backend_is_not_python)
import struct

__all__ = [
    'find',
    'Crypto'
]

PRIME_NUMBER, MOD = 257, 1000000007

def find(text, query, algorithm, **kwargs):
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

        'rabin_karp' -> Rabin–Karp algorithm as given in [2].

        'boyer_moore' -> Boyer-Moore algorithm as given in [3].

        'z_function' -> Z-function algorithm as given in [4].

    backend: pydatastructs.Backend
        The backend to be used.
        Optional, by default, the best available
        backend is used.

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

    .. [1] https://en.wikipedia.org/wiki/Knuth%E2%80%93Morris%E2%80%93Pratt_algorithm
    .. [2] https://en.wikipedia.org/wiki/Rabin%E2%80%93Karp_algorithm
    .. [3] https://en.wikipedia.org/wiki/Boyer%E2%80%93Moore_string-search_algorithm
    .. [4] https://usaco.guide/CPH.pdf#page=257
    """
    raise_if_backend_is_not_python(
            find, kwargs.get('backend', Backend.PYTHON))
    import pydatastructs.strings.algorithms as algorithms
    func = "_" + algorithm
    if not hasattr(algorithms, func):
        raise NotImplementedError(
        "Currently %s algoithm for searching strings "
        "inside a text isn't implemented yet."
        %(algorithm))
    return getattr(algorithms, func)(text, query)


def _knuth_morris_pratt(text, query):
    if len(text) == 0 or len(query) == 0:
        return DynamicOneDimensionalArray(int, 0)
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

def _p_pow(length, p=PRIME_NUMBER, m=MOD):
    p_pow = OneDimensionalArray(int, length)
    p_pow[0] = 1
    for i in range(1, length):
        p_pow[i] = (p_pow[i-1] * p) % m
    return p_pow

def _hash_str(string, p=PRIME_NUMBER, m=MOD):
    hash_value = 0
    p_pow = _p_pow(len(string), p, m)
    for i in range(len(string)):
        hash_value = (hash_value + ord(string[i]) * p_pow[i]) % m
    return hash_value

def _rabin_karp(text, query):
    t = len(text)
    q = len(query)
    positions = DynamicOneDimensionalArray(int, 0)
    if q == 0 or t == 0:
        return positions

    query_hash = _hash_str(query)
    text_hash = OneDimensionalArray(int, t + 1)
    text_hash.fill(0)
    p_pow = _p_pow(t)

    for i in range(t):
        text_hash[i+1] = (text_hash[i] + ord(text[i]) * p_pow[i]) % MOD
    for i in range(t - q + 1):
        curr_hash = (text_hash[i + q] + MOD - text_hash[i]) % MOD
        if curr_hash == (query_hash * p_pow[i]) % MOD:
            positions.append(i)

    return positions

def _boyer_moore(text, query):
    positions = DynamicOneDimensionalArray(int, 0)
    text_length, query_length = len(text), len(query)

    if text_length == 0 or query_length == 0:
        return positions

    # Preprocessing Step
    bad_match_table = dict()
    for i in range(query_length):
        bad_match_table[query[i]] = i

    shift = 0
    # Matching procedure
    while shift <= text_length-query_length:
        j = query_length - 1
        while j >= 0 and query[j] == text[shift + j]:
            j -= 1
        if j < 0:
            positions.append(shift)
            if shift + query_length < text_length:
                if text[shift + query_length] in bad_match_table:
                    shift += query_length - bad_match_table[text[shift + query_length]]
                else:
                    shift += query_length + 1
            else:
                shift += 1
        else:
            letter_pos = text[shift + j]
            if letter_pos in bad_match_table:
                shift += max(1, j - bad_match_table[letter_pos])
            else:
                shift += max(1, j + 1)
    return positions

def _z_vector(text, query):
    string = text
    if query != "":
        string = query + str("$") + text

    z_fct = OneDimensionalArray(int, len(string))
    z_fct.fill(0)

    curr_pos = 1
    seg_left = 0
    seg_right = 0

    for curr_pos in range(1,len(string)):
        if curr_pos <= seg_right:
            z_fct[curr_pos] = min(seg_right - curr_pos + 1, z_fct[curr_pos - seg_left])

        while curr_pos + z_fct[curr_pos] < len(string) and \
                string[z_fct[curr_pos]] == string[curr_pos + z_fct[curr_pos]]:
            z_fct[curr_pos] += 1

        if curr_pos + z_fct[curr_pos] - 1 > seg_right:
            seg_left = curr_pos
            seg_right = curr_pos + z_fct[curr_pos] - 1

    final_z_fct = DynamicOneDimensionalArray(int, 0)
    start_index = 0
    if query != "":
        start_index = len(query) + 1
    for pos in range(start_index, len(string)):
        final_z_fct.append(z_fct[pos])

    return final_z_fct

def _z_function(text, query):
    positions = DynamicOneDimensionalArray(int, 0)
    if len(text) == 0 or len(query) == 0:
        return positions

    fct = _z_vector(text, query)
    for pos in range(len(fct)):
        if fct[pos] == len(query):
            positions.append(pos)

    return positions

class Crypto:

    @staticmethod
    def _right_rotate(value, shift, size=32):
        return (value >> shift) | (value << (size - shift)) & (2**size - 1)

    @staticmethod
    def sha256_encrypt(text) -> str:
        """
        Finds the SHA256 ciphertext of the given plaintext

        Parameters
        ==========

        text: str
            The string on which SHA256 encryption is to be performed.

        Returns
        =======

        text: str
            The SHA256 encoded ciphertext

        Examples
        ========

        >>> from pydatastructs.strings.algorithms import Crypto
        >>> text = "PyDataStructs"
        >>> ciphertext = Crypto.sha256_encrypt(text)
        >>> print(ciphertext)
        "777a305fe4f1cfc7ce270891ec50651331e2ab6d09312b906740a5ea413bd057"

        References
        ==========

        .. [1] https://en.wikipedia.org/wiki/SHA-2
        .. [2] https://github.com/TheAlgorithms/Python/blob/master/hashes/sha256.py

        """
        # SHA-256 Constants
        k = [
            0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
            0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
            0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
            0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
            0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
            0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
            0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
            0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
        ]
        
        h = [
            0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
            0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
        ]
        
        message = bytearray(text, 'utf-8')
        length = len(message) * 8
        message.append(0x80)
        while (len(message) * 8) % 512 != 448:
            message.append(0)
        message += struct.pack('>Q', length)
        
        for i in range(0, len(message), 64):
            chunk = message[i:i+64]
            w = list(struct.unpack('>16L', chunk)) + [0] * 48
            for j in range(16, 64):
                s0 = (Crypto._right_rotate(w[j-15], 7) ^ Crypto._right_rotate(w[j-15], 18) ^ (w[j-15] >> 3))
                s1 = (Crypto._right_rotate(w[j-2], 17) ^ Crypto._right_rotate(w[j-2], 19) ^ (w[j-2] >> 10))
                w[j] = (w[j-16] + s0 + w[j-7] + s1) & 0xFFFFFFFF
            
            a, b, c, d, e, f, g, h0 = h
            
            for j in range(64):
                S1 = Crypto._right_rotate(e, 6) ^ Crypto._right_rotate(e, 11) ^ Crypto._right_rotate(e, 25)
                ch = (e & f) ^ (~e & g)
                temp1 = (h0 + S1 + ch + k[j] + w[j]) & 0xFFFFFFFF
                S0 = Crypto._right_rotate(a, 2) ^ Crypto._right_rotate(a, 13) ^ Crypto._right_rotate(a, 22)
                maj = (a & b) ^ (a & c) ^ (b & c)
                temp2 = (S0 + maj) & 0xFFFFFFFF
                
                h0, g, f, e, d, c, b, a = (g, f, e, (d + temp1) & 0xFFFFFFFF, c, b, a, (temp1 + temp2) & 0xFFFFFFFF)
            
            h = [(x + y) & 0xFFFFFFFF for x, y in zip(h, [a, b, c, d, e, f, g, h0])]
        
        return ''.join(f'{value:08x}' for value in h)