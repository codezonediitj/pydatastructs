import unittest
from pydatastructs.linear_data_structures.circular_buffer import CircularBuffer

class TestCircularBuffer(unittest.TestCase):

    def setUp(self):
        self.buffer = CircularBuffer(3, dtype=int)  # Added dtype argument

    def test_enqueue_dequeue(self):
        self.buffer.enqueue(1)
        self.buffer.enqueue(2)
        self.assertEqual(self.buffer.dequeue(), 1)
        self.assertEqual(self.buffer.dequeue(), 2)

    def test_is_empty(self):
        self.assertTrue(self.buffer.is_empty())
        self.buffer.enqueue(1)
        self.assertFalse(self.buffer.is_empty())

    def test_is_full(self):
        self.buffer.enqueue(1)
        self.buffer.enqueue(2)
        self.buffer.enqueue(3)
        self.assertTrue(self.buffer.is_full())

    def test_peek(self):
        self.buffer.enqueue(1)
        self.buffer.enqueue(2)
        self.assertEqual(self.buffer.peek(), 1)

    def test_enqueue_overflow(self):
        self.buffer.enqueue(1)
        self.buffer.enqueue(2)
        self.buffer.enqueue(3)
        with self.assertRaises(OverflowError):
            self.buffer.enqueue(4)

    def test_dequeue_underflow(self):
        with self.assertRaises(ValueError):
            self.buffer.dequeue()

if __name__ == '__main__':
    unittest.main()
