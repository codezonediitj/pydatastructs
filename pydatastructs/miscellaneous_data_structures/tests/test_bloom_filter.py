from pydatastructs.miscellaneous_data_structures import BloomFilter
from pydatastructs.miscellaneous_data_structures.bloom_filter import BitArray
from pydatastructs.utils.raises_util import raises
from pydatastructs.utils.misc_util import _check_type, Backend

def test_BloomFilter():
    assert raises(ValueError, lambda: BloomFilter(capacity=10**5, error_rate=0))
    assert raises(ValueError, lambda: BloomFilter(capacity=10**5, error_rate=1))
    assert raises(ValueError, lambda: BloomFilter(capacity=0, error_rate=0.005))

    bf = BloomFilter(capacity=10**5, error_rate=0.005)
    bf.add(1)
    assert 1 in bf
    bf.add("Q")
    assert "Q" in bf
    assert "q" not in bf
    assert len(bf) == 2
    assert 1 in bf

    bf.add(True)
    assert True in bf
    assert False not in bf

    bf = BloomFilter(capacity=10**2, error_rate=0.002, array_size=10**6, num_hashes=5, hash_name='md5')
    bf.add(1.0)
    assert 1 not in bf
    bf.add("Q")
    assert "p" not in bf
    assert "Q" in bf
    bf.add(False)
    assert len(bf) == 3
    assert False in bf

    bf = BloomFilter(capacity=10**2, init_elements=[1, 2, 3, 4, 5])
    assert 1 in bf
    assert 2 in bf
    assert 3 in bf
    assert len(bf) == 5

    bf.add(b'q')
    assert b'q' in bf
    assert b'Q' not in bf

    bf = BloomFilter(capacity=1, init_elements=[], backend=Backend.PYTHON)
    bf.add(1)
    assert raises(ValueError, lambda: bf.add(2))

def test_BitArray():
    ba = BitArray(10, bits_per_slice=8)
    assert ba[0] == ba[1] == ba[2] == ba[3] == ba[4] == ba[5] == ba[6] == ba[7] == ba[8] == ba[9] == 0
    ba[0] = 1
    assert ba[0] == 1
    assert ba[1] == ba[2] == ba[3] == ba[4] == ba[5] == ba[6] == ba[7] == ba[8] == ba[9] == 0
    ba[1] = 1
    assert ba[0] == ba[1] == 1
    assert ba[2] == ba[3] == ba[4] == ba[5] == ba[6] == ba[7] == ba[8] == ba[9] == 0
    ba[9] = 1
    assert ba[0] == ba[1] == ba[9] == 1
    assert ba[2] == ba[3] == ba[4] == ba[5] == ba[6] == ba[7] == ba[8] == 0
    ba[0] = 0
    assert ba[0] == ba[2] == ba[3] == ba[4] == ba[5] == ba[6] == ba[7] == ba[8] == 0
    assert ba[1] == ba[9] == 1
    ba[1] = 0
    assert ba[0] == ba[1] == ba[2] == ba[3] == ba[4] == ba[5] == ba[6] == ba[7] == ba[8] == 0
    assert ba[9] == 1
    ba[9] = 0
    assert ba[0] == ba[1] == ba[2] == ba[3] == ba[4] == ba[5] == ba[6] == ba[7] == ba[8] == ba[9] == 0

    assert raises(IndexError, lambda: ba[10])
    assert raises(IndexError, lambda: ba[-1])

    def set():
        ba[10] = 1
    assert raises(IndexError, set)

    assert raises(ValueError, lambda: BitArray(10, bits_per_slice=0))
    assert raises(ValueError, lambda: BitArray(0, bits_per_slice=2))
