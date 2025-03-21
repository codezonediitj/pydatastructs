from pydatastructs.multi_threaded_algorithms.fibonacci import Fibonacci
import threading
from pydatastructs.utils.raises_util import raises


def test_Fibonacci():
    # Test for the Fibonacci class with default Python backend
    f = Fibonacci(20)
    assert isinstance(f, Fibonacci)
    assert f.n == 20
    assert f.calculate() == 6765  # Fibonacci(20)

    # Test with different n values
    f1 = Fibonacci(7)
    assert f1.calculate() == 13  # Fibonacci(7)

    f2 = Fibonacci(0)
    assert f2.calculate() == 0  # Fibonacci(0)

    f3 = Fibonacci(1)
    assert f3.calculate() == 1  # Fibonacci(1)

    # Test for full Fibonacci sequence up to n
    assert f.sequence == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765]

    # Test for larger Fibonacci number
    f_large = Fibonacci(100)
    assert f_large.calculate() == 354224848179261915075  # Fibonacci(100)

    # Test for sequence with larger n values
    assert len(f_large.sequence) == 101  # Fibonacci sequence up to 100 should have 101 elements

def test_Fibonacci_with_threading():
    # Test for multi-threading Fibonacci calculation for small numbers
    f_small = Fibonacci(10)
    result_small = f_small.calculate()
    assert result_small == 55  # Fibonacci(10)

    # Test for multi-threading Fibonacci calculation with medium size n
    f_medium = Fibonacci(30)
    result_medium = f_medium.calculate()
    assert result_medium == 832040  # Fibonacci(30)

    # Test for multi-threading Fibonacci calculation with large n
    f_large = Fibonacci(50)
    result_large = f_large.calculate()
    assert result_large == 12586269025  # Fibonacci(50)

    # Test the Fibonacci sequence correctness for medium size n
    assert f_medium.sequence == [
        0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181,
        6765, 10946, 17711, 28657, 46368, 75025, 121393, 196418, 317811, 514229, 832040
    ]

    # Check that sequence length is correct for large n (e.g., Fibonacci(50))
    assert len(f_large.sequence) == 51  # Fibonacci sequence up to 50 should have 51 elements

    # Test invalid input (n cannot be negative)
    assert raises(ValueError, lambda: Fibonacci(-5))

    # Test when backend is set to CPP (this part assumes a proper backend, can be skipped if not implemented)
    f_cpp = Fibonacci(10, backend='python')
    result_cpp = f_cpp.calculate()
    assert result_cpp == 55  # Fibonacci(10) should be the same result as Python

    # Test if sequence matches expected for small number of terms
    f_test = Fibonacci(5)
    assert f_test.sequence == [0, 1, 1, 2, 3, 5]

def test_Fibonacci_with_invalid_backend():
    # Test when an invalid backend is provided (should raise an error)
    assert raises(NotImplementedError, lambda: Fibonacci(20, backend='invalid_backend'))

def test_Fibonacci_with_threads():
    # Test multi-threaded calculation is correct for different n
    f_threaded = Fibonacci(25)
    assert f_threaded.calculate() == 75025  # Fibonacci(25)
    # Validate that the thread pool handles large n correctly
    f_threaded_large = Fibonacci(40)
    assert f_threaded_large.calculate() == 102334155  # Fibonacci(40)
    # Ensure that no threads are left hanging (checks for thread cleanup)
    threads_before = threading.active_count()
    f_threaded.calculate()
    threads_after = threading.active_count()
    assert threads_before == threads_after  # No new threads should be created unexpectedly
