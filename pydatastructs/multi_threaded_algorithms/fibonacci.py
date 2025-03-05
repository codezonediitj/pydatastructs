import threading

class Fibonacci:
    """Representation of Fibonacci data structure

    Parameters
    ----------
    n : int
        The index for which to compute the Fibonacci number.
    backend : str
        Optional, by default 'python'. Specifies whether to use the Python implementation or another backend.
    """

    def __init__(self, n, backend='python'):
        if n<0:
            raise ValueError("n cannot be negative")
        self.n = n
        self.backend = backend
        self.result = [None] * (n + 1)  # To store Fibonacci numbers
        self.threads = []  # List to store thread references
        # Check for valid backend
        if backend != 'python':
            raise NotImplementedError(f"Backend '{backend}' is not implemented.")

    def fib(self, i):
        """Calculates the Fibonacci number recursively and stores it in result."""
        if i <= 1:
            return i
        if self.result[i] is not None:
            return self.result[i]
        self.result[i] = self.fib(i - 1) + self.fib(i - 2)
        return self.result[i]

    def threaded_fib(self, i):
        """Wrapper function to calculate Fibonacci in a thread and store the result."""
        self.result[i] = self.fib(i)

    def calculate(self):
        """Calculates the Fibonacci sequence for all numbers up to n using multi-threading."""
        # Start threads for each Fibonacci number calculation
        for i in range(self.n + 1):
            thread = threading.Thread(target=self.threaded_fib, args=(i,))
            self.threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in self.threads:
            thread.join()

        # Return the nth Fibonacci number after all threads complete
        return self.result[self.n]

    @property
    def sequence(self):
        """Returns the Fibonacci sequence up to the nth number."""
        return self.result[:self.n + 1]
