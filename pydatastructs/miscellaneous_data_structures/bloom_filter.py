from pydatastructs.linear_data_structures import OneDimensionalArray # TODO: Use a C++ Backend for the BitArray class
from pydatastructs.utils.misc_util import (
    Backend, raise_if_backend_is_not_python)
import hashlib
import math


__all__ = ['BloomFilter']

class BloomFilter(object):
    """
    Represents a Bloom Filter for Probabilistic Membership testing

    Parameters
    ==========

    capacity: int
        The capacity of the Bloom Filter. i.e., the maximum number of elements the filter can hold not exceeding the error rate.

    error_rate: float
        The error rate of the Bloom Filter. i.e., the probability of false positives.

    backend: pydatastructs.Backend
        The backend to be used.
        Optional, by default, the best available
        backend is used.

    Examples
    ========

    >>> from pydatastructs import BloomFilter
    >>> bf = BloomFilter(capacity=10**5, error_rate=0.005)
    >>> bf.add(1)
    >>> 1 in bf
    True
    >>> bf.add("Hello")
    >>> "Hello" in bf
    True
    >>> "hello" in bf
    False
    >>> len(bf)
    2

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Bloom_filter
    """

    BITS_PER_SLICE = 32

    __slots__ = ['barray', 'array_size', 'capacity', 'num_hashes', 'hash_name', 'n_ele']

    def __new__(cls, capacity=10**5, error_rate=0.005, array_size=None, num_hashes=None, hash_name='sha512', init_elements=None, **kwargs):
        raise_if_backend_is_not_python(
            cls, kwargs.get('backend', Backend.PYTHON))

        if not (1 > error_rate > 0):
            raise ValueError("Error Rate must be between 0 and 1.")
        if not capacity > 0:
            raise ValueError("Capacity must be gerater than 0")

        obj = object.__new__(cls)
        if array_size is None:
            array_size = math.ceil((capacity * abs(math.log(error_rate))) / (math.log(2) ** 2))
        obj.array_size = array_size
        obj.barray = BitArray(obj.array_size, cls.BITS_PER_SLICE)
        obj.hash_name = hash_name
        obj.capacity = capacity
        obj.n_ele = 0
        if num_hashes is None:
            num_hashes = math.ceil((obj.array_size / capacity) * math.log(2))
        obj.num_hashes = num_hashes

        if init_elements is not None:
            for elem in init_elements:
                obj.add(elem)

        return obj

    @classmethod
    def methods(cls):
        return ['add', '__new__', 'contains', '__contains__']

    def add(self, key):
        """
        Adds the key to the Bloom Filter

        Parameters
        ==========
        key: str | bytes | int | float | bool
            The key to be added to the Bloom Filter
        """

        if self.n_ele >= self.capacity:
            raise ValueError("Bloom Filter is full")

        key = self._serialize(key)
        for h in self._hashes(key):
            self.barray[h] = 1
        self.n_ele += 1

    def contains(self, key):
        """
        Checks if the Bloom Filter contains the key

        Parameters
        ==========

        key: str | bytes | int | float | bool
            The key to be checked for membership
        """

        key = self._serialize(key)
        for h in self._hashes(key):
            if self.barray[h] == 0:
                return False
        return True

    def _serialize(self, data):
        if isinstance(data, bytes):
            return data
        elif isinstance(data, str):
            return data.encode('utf-8')
        elif isinstance(data, (int, float, bool)):
            return str(data).encode('utf-8')
        else:
            raise TypeError(f"Data type {type(data)} not supported")


    def _hashes(self, data: bytes):
        result = []
        salt = 0

        while len(result) < self.num_hashes:
            hasher = hashlib.new(self.hash_name)
            hasher.update(bytes([salt]))
            hasher.update(data)
            digest = hasher.digest()
            salt += 1

            for i in range(0, len(digest), 4):
                if len(result) >= self.num_hashes:
                    break
                h = int.from_bytes(digest[i:i+4], byteorder="big", signed=False) % self.array_size
                result.append(h)

        return result

    def __len__(self):
        return self.n_ele

    def __contains__(self, data):
        return self.contains(data)



class BitArray():
    def __init__(self, size, bits_per_slice=32):
        if bits_per_slice <= 0:
            raise ValueError("Bits per slice must be greater than 0")
        if size <= 0:
            raise ValueError("Size must be greater than 0")

        self.size = size
        self.byte_size = (size + bits_per_slice - 1) // bits_per_slice
        self.b = bits_per_slice
        self.array = OneDimensionalArray(int, size, init=0)

    def __setitem__(self, i, value):
        if i >= self.size:
            raise IndexError("Index out of range")

        byte_index = i // self.b
        bit_index = i % self.b

        current_value = self.array[byte_index]

        if value:
            current_value |= (1 << bit_index)
        else:
            current_value &= ~(1 << bit_index)

        self.array[byte_index] = current_value

    def __getitem__(self, i):
        if i >= self.size:
            raise IndexError("Index out of range")

        byte_index = i // self.b
        bit_index = i % self.b

        return (self.array[byte_index] >> bit_index) & 1
