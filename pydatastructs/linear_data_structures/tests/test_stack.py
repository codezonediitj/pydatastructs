
import unittest

from pydatastructs.linear_data_structures import Stack

class TestStack(unittest.TestCase):
    """Stack Tests"""
    def setUp(self):
        """Set Up"""
        self.s = Stack(max_size=5, type_restriction=['int', 'str'])

    def test_length(self):
        """"""
        self.s.push('2')
        self.s.push('A')
        self.assertEqual(len(self.s), 2)
        self.s.pop()
        self.assertEqual(len(self.s), 1)

    def test_error_init(self):
        """Testing Errors in init"""
        with self.assertRaises(TypeError):
            stack_temp = Stack(type_restriction='int')
        with self.assertRaises(TypeError):
            stack_temp = Stack(type_restriction=[int])
        with self.assertRaises(TypeError):
            stack_temp = Stack(max_size='10')

    def test_push_pop(self):
        """Testing consecutive push and pop"""
        self.s.push(2)
        self.s.push(1)
        self.assertEqual(self.s.pop(), 1)
        self.assertEqual(self.s.pop(), 2)

    def test_stack_overflow(self):
        """Testing Stack overflow condition"""
        self.s.push(2)
        self.s.push(1)
        self.s.push(3)
        self.s.push(4)
        self.s.push(5)
        with self.assertRaises(ValueError):
            self.s.push(6)

    def test_stack_underflow(self):
        """Testing Stack underflow condition"""
        self.s.push(2)
        self.s.push(1)
        self.assertEqual(self.s.pop(), 1)
        self.assertEqual(self.s.pop(), 2)
        with self.assertRaises(ValueError):
            self.s.pop()

    def tearDown(self):
        """Tear Down"""
        del self.s
