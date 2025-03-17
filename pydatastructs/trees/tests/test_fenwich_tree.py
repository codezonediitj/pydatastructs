import unittest
from pydatastructs import fenwich_tree

class TestFenwickTree(unittest.TestCase):

    def test_initialization_with_size(self):
        ft = fenwich_tree(5)
        self.assertEqual(ft.size, 5)
        self.assertEqual(ft.tree, [0, 0, 0, 0, 0, 0])
        self.assertEqual(ft.original_array, [0, 0, 0, 0, 0])

    def test_initialization_with_array(self):
        arr = [1, 2, 3, 4, 5]
        ft = fenwich_tree(arr)
        self.assertEqual(ft.size, 5)
        self.assertEqual(ft.original_array, arr)
        # Manually calculate prefix sums and check the tree structure
        expected_tree = [0, 1, 3, 3, 10, 5]
        self.assertEqual(ft.tree, expected_tree)

    def test_initialization_with_empty_array(self):
        arr = []
        ft = fenwich_tree(arr)
        self.assertEqual(ft.size, 0)
        self.assertEqual(ft.tree, [0])
        self.assertEqual(ft.original_array, [])

    def test_initialization_with_invalid_input(self):
        with self.assertRaises(ValueError):
            fenwich_tree("invalid")

    def test_update_single_element(self):
        ft = fenwich_tree([1, 2, 3, 4, 5])
        ft.update(1, 10)
        self.assertEqual(ft.original_array, [1, 10, 3, 4, 5])
        expected_tree = [0, 1, 11, 3, 18, 5]
        self.assertEqual(ft.tree, expected_tree)

    def test_update_out_of_bounds(self):
        ft = fenwich_tree(5)
        with self.assertRaises(IndexError):
            ft.update(5, 10)
        with self.assertRaises(IndexError):
            ft.update(-1, 10)

    def test_prefix_sum_positive_indices(self):
        arr = [1, 2, 3, 4, 5]
        ft = fenwich_tree(arr)
        self.assertEqual(ft.prefix_sum(0), 1)
        self.assertEqual(ft.prefix_sum(1), 3)
        self.assertEqual(ft.prefix_sum(2), 6)
        self.assertEqual(ft.prefix_sum(3), 10)
        self.assertEqual(ft.prefix_sum(4), 15)

    def test_prefix_sum_out_of_bounds(self):
        ft = fenwich_tree(5)
        with self.assertRaises(IndexError):
            ft.prefix_sum(5)
        with self.assertRaises(IndexError):
            ft.prefix_sum(-1)

    def test_prefix_sum_empty_array(self):
        ft = fenwich_tree([])
        with self.assertRaises(IndexError):
            ft.prefix_sum(0) # Should raise IndexError as size is 0

    def test_range_sum_valid_range(self):
        arr = [1, 2, 3, 4, 5]
        ft = fenwich_tree(arr)
        self.assertEqual(ft.range_sum(0, 0), 1)
        self.assertEqual(ft.range_sum(0, 1), 3)
        self.assertEqual(ft.range_sum(1, 3), 2 + 3 + 4)
        self.assertEqual(ft.range_sum(2, 4), 3 + 4 + 5)
        self.assertEqual(ft.range_sum(0, 4), 1 + 2 + 3 + 4 + 5)

    def test_range_sum_out_of_bounds(self):
        ft = fenwich_tree(5)
        with self.assertRaises(IndexError):
            ft.range_sum(0, 5)
        with self.assertRaises(IndexError):
            ft.range_sum(-1, 2)
        with self.assertRaises(IndexError):
            ft.range_sum(1, 5)
        with self.assertRaises(IndexError):
            ft.range_sum(-1, -1)

    def test_range_sum_invalid_range(self):
        ft = fenwich_tree(5)
        with self.assertRaises(IndexError):
            ft.range_sum(3, 1)

    def test_range_sum_single_element(self):
        arr = [10, 20, 30]
        ft = fenwich_tree(arr)
        self.assertEqual(ft.range_sum(0, 0), 10)
        self.assertEqual(ft.range_sum(1, 1), 20)
        self.assertEqual(ft.range_sum(2, 2), 30)

    def test_range_sum_entire_array(self):
        arr = [1, 2, 3, 4, 5]
        ft = fenwich_tree(arr)
        self.assertEqual(ft.range_sum(0, ft.size - 1), 15)

    def test_update_and_query_sequence(self):
        ft = fenwich_tree([2, 5, 1, 8, 3])
        self.assertEqual(ft.prefix_sum(3), 2 + 5 + 1 + 8)  # 16
        ft.update(1, 10)
        self.assertEqual(ft.prefix_sum(3), 2 + 10 + 1 + 8) # 21
        self.assertEqual(ft.range_sum(0, 2), 2 + 10 + 1)   # 13
        ft.update(4, 0)
        self.assertEqual(ft.prefix_sum(4), 2 + 10 + 1 + 8 + 0) # 21
        self.assertEqual(ft.range_sum(3, 4), 8 + 0)       # 8
