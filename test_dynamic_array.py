import unittest
from typing import List

from hypothesis import given, strategies as st

from dynamic_array import DynamicArray


class TestDynamicArray(unittest.TestCase):
    """Test functionality of the DynamicArray class."""
    def test_empty(self) -> None:
        """Test creating an empty array."""
        arr = DynamicArray.empty()
        self.assertEqual(arr.length(), 0)
        self.assertEqual(str(arr), "[]")

    def test_from_list(self) -> None:
        """Test creating array from a list."""
        arr = DynamicArray.from_list([1, 2, 3])
        self.assertEqual(arr.length(), 3)
        self.assertEqual(str(arr), "[1, 2, 3]")

    def test_cons(self) -> None:
        """Test cons operation."""
        arr = DynamicArray.empty()
        arr = arr.cons(3).cons(2).cons(1)
        self.assertEqual(arr.length(), 3)
        self.assertEqual(str(arr), "[1, 2, 3]")

    def test_remove(self) -> None:
        """Test remove operation."""
        arr = DynamicArray.from_list([1, 2, 3, 2])
        arr = arr.remove(2)
        self.assertEqual(str(arr), "[1, 3, 2]")
        # Test removing non-existent element
        arr = arr.remove(4)
        self.assertEqual(str(arr), "[1, 3, 2]")

    def test_length(self) -> None:
        """Test length operation."""
        arr = DynamicArray.from_list([1, 2, 3])
        self.assertEqual(arr.length(), 3)
        arr = arr.cons(0)
        self.assertEqual(arr.length(), 4)

    def test_member(self) -> None:
        """Test member operation."""
        arr = DynamicArray.from_list([1, 2, 3])
        self.assertTrue(arr.member(1))
        self.assertTrue(arr.member(2))
        self.assertTrue(arr.member(3))
        self.assertFalse(arr.member(4))

    def test_reverse(self) -> None:
        """Test reverse operation."""
        arr = DynamicArray.from_list([1, 2, 3])
        reversed_arr = arr.reverse()
        self.assertEqual(str(reversed_arr), "[3, 2, 1]")
        # Original array remains unchanged
        self.assertEqual(str(arr), "[1, 2, 3]")

    def test_to_list(self) -> None:
        """Test to_list operation."""
        arr = DynamicArray.from_list([1, 2, 3])
        self.assertEqual(arr.to_list(), [1, 2, 3])

    def test_get(self) -> None:
        """Test get operation."""
        arr = DynamicArray.from_list([1, 2, 3])
        self.assertEqual(arr.get(0), 1)
        self.assertEqual(arr.get(1), 2)
        self.assertEqual(arr.get(2), 3)
        # Test negative indexing
        self.assertEqual(arr.get(-1), 3)
        self.assertEqual(arr.get(-2), 2)
        self.assertEqual(arr.get(-3), 1)
        # Test index out of bounds
        with self.assertRaises(IndexError):
            arr.get(3)
        with self.assertRaises(IndexError):
            arr.get(-4)

    def test_set(self) -> None:
        """Test set operation."""
        arr = DynamicArray.from_list([1, 2, 3])
        new_arr = arr.set(1, 5)
        # New array is updated
        self.assertEqual(str(new_arr), "[1, 5, 3]")
        # Original array remains unchanged
        self.assertEqual(str(arr), "[1, 2, 3]")
        # Test negative indexing
        new_arr = arr.set(-1, 6)
        self.assertEqual(str(new_arr), "[1, 2, 6]")
        # Test index out of bounds
        with self.assertRaises(IndexError):
            arr.set(3, 7)
        with self.assertRaises(IndexError):
            arr.set(-4, 7)

    def test_filter(self) -> None:
        """Test filter operation."""
        arr = DynamicArray.from_list([1, 2, 3, 4, 5])
        filtered = arr.filter(lambda x: x % 2 == 0)
        self.assertEqual(str(filtered), "[2, 4]")
        # Original array remains unchanged
        self.assertEqual(str(arr), "[1, 2, 3, 4, 5]")

    def test_map(self) -> None:
        """Test map operation."""
        arr = DynamicArray.from_list([1, 2, 3])
        mapped = arr.map(lambda x: x * 2)
        self.assertEqual(str(mapped), "[2, 4, 6]")
        # Original array remains unchanged
        self.assertEqual(str(arr), "[1, 2, 3]")

    def test_reduce(self) -> None:
        """Test reduce operation."""
        arr = DynamicArray.from_list([1, 2, 3, 4])
        sum_result = arr.reduce(lambda acc, x: acc + x, 0)
        self.assertEqual(sum_result, 10)
        product_result = arr.reduce(lambda acc, x: acc * x, 1)
        self.assertEqual(product_result, 24)

    def test_iterator(self) -> None:
        """Test iterator operation."""
        arr = DynamicArray.from_list([1, 2, 3])
        iterator = arr.iterator()
        self.assertEqual(next(iterator), 1)
        self.assertEqual(next(iterator), 2)
        self.assertEqual(next(iterator), 3)
        with self.assertRaises(StopIteration):
            next(iterator)

    def test_intersection(self) -> None:
        """Test intersection operation."""
        arr1 = DynamicArray.from_list([1, 2, 3, 4])
        arr2 = DynamicArray.from_list([3, 4, 5, 6])
        intersection = arr1.intersection(arr2)
        self.assertEqual(str(intersection), "[3, 4]")
        # Original arrays remain unchanged
        self.assertEqual(str(arr1), "[1, 2, 3, 4]")
        self.assertEqual(str(arr2), "[3, 4, 5, 6]")

    def test_concat(self) -> None:
        """Test concat operation."""
        arr1 = DynamicArray.from_list([1, 2])
        arr2 = DynamicArray.from_list([3, 4])
        concatenated = arr1.concat(arr2)
        self.assertEqual(str(concatenated), "[1, 2, 3, 4]")
        # Original arrays remain unchanged
        self.assertEqual(str(arr1), "[1, 2]")
        self.assertEqual(str(arr2), "[3, 4]")

    def test_eq(self) -> None:
        """Test __eq__ operation."""
        arr1 = DynamicArray.from_list([1, 2, 3])
        arr2 = DynamicArray.from_list([1, 2, 3])
        arr3 = DynamicArray.from_list([1, 2, 4])
        self.assertEqual(arr1, arr2)
        self.assertNotEqual(arr1, arr3)
        self.assertNotEqual(arr1, "not an array")

    def test_str(self) -> None:
        """Test __str__ operation."""
        arr = DynamicArray.from_list([1, None, 3])
        self.assertEqual(str(arr), "[1, None, 3]")

    def test_iter(self) -> None:
        """Test __iter__ operation."""
        arr = DynamicArray.from_list([1, 2, 3])
        items = []
        for item in arr:
            items.append(item)
        self.assertEqual(items, [1, 2, 3])

    def test_none_values(self) -> None:
        """Test handling of None values."""
        arr = DynamicArray.from_list([None, 1, None, 3])
        self.assertEqual(arr.length(), 4)
        self.assertEqual(str(arr), "[None, 1, None, 3]")
        # Test membership check for None
        self.assertTrue(arr.member(None))
        # Test removing None values
        arr_without_none = arr.remove(None)
        self.assertEqual(str(arr_without_none), "[1, None, 3]")

    def test_empty_operations(self) -> None:
        """Test operations on empty arrays."""
        empty_arr = DynamicArray.empty()
        # Test basic operations on empty array
        self.assertEqual(empty_arr.length(), 0)
        self.assertFalse(empty_arr.member(1))
        self.assertEqual(empty_arr.to_list(), [])
        # Test reverse of empty array
        self.assertEqual(empty_arr.reverse().to_list(), [])
        # Test filter and map on empty array
        self.assertEqual(empty_arr.filter(lambda x: True).to_list(), [])
        self.assertEqual(empty_arr.map(lambda x: x * 2).to_list(), [])
        # Test reduce on empty array
        self.assertEqual(empty_arr.reduce(lambda acc, x: acc + x, 0), 0)
        # Test concat with empty array
        arr = DynamicArray.from_list([1, 2])
        self.assertEqual(empty_arr.concat(arr).to_list(), [1, 2])
        self.assertEqual(arr.concat(empty_arr).to_list(), [1, 2])

    def test_growth_factor_one(self) -> None:
        """Test resizing behavior when growth_factor=1."""
        arr = DynamicArray.empty(growth_factor=1.0)
        # Add elements sequentially to observe resizing
        for i in range(5):
            arr = arr.cons(i)
        self.assertEqual(arr.length(), 5)
        self.assertEqual(arr.to_list(), [4, 3, 2, 1, 0])

    def test_api(self) -> None:
        """User-provided API test."""
        # Create empty array
        empty_array = DynamicArray.empty()
        self.assertEqual(empty_array.length(), 0)
        # Create array from list
        array_from_list = DynamicArray.from_list([1, 2, 3])
        self.assertEqual(array_from_list.length(), 3)
        # Add element
        new_array = array_from_list.cons(0)
        self.assertEqual(new_array.length(), 4)
        self.assertEqual(new_array.get(0), 0)
        # Remove element
        array_without_2 = array_from_list.remove(2)
        self.assertEqual(array_without_2.length(), 2)
        self.assertEqual(array_without_2.to_list(), [1, 3])
        # Check membership
        self.assertTrue(array_from_list.member(2))
        self.assertFalse(array_from_list.member(4))
        # Reverse array
        reversed_array = array_from_list.reverse()
        self.assertEqual(reversed_array.to_list(), [3, 2, 1])
        # Set element
        modified_array = array_from_list.set(1, 5)
        self.assertEqual(modified_array.to_list(), [1, 5, 3])
        # Filter elements
        filtered_array = array_from_list.filter(lambda x: x > 1)
        self.assertEqual(filtered_array.to_list(), [2, 3])
        # Map elements
        mapped_array = array_from_list.map(lambda x: x * 2)
        self.assertEqual(mapped_array.to_list(), [2, 4, 6])
        # Reduce elements
        sum_result = array_from_list.reduce(lambda acc, x: acc + x, 0)
        self.assertEqual(sum_result, 6)
        # Array intersection
        array1 = DynamicArray.from_list([1, 2, 3])
        array2 = DynamicArray.from_list([2, 3, 4])
        intersection_array = array1.intersection(array2)
        self.assertEqual(intersection_array.to_list(), [2, 3])
        # Array concatenation
        concatenated_array = array1.concat(array2)
        self.assertEqual(concatenated_array.to_list(), [1, 2, 3, 2, 3, 4])


class MonoidLawsTest(unittest.TestCase):
    """Test Monoid laws."""
    @given(st.lists(st.integers()),
           st.lists(st.integers()),
           st.lists(st.integers()))
    def test_monoid_laws(self, list_x: List[int],
                         list_y: List[int], list_z: List[int]) -> None:
        """Test Monoid laws using Hypothesis."""
        x = DynamicArray.from_list(list_x)
        y = DynamicArray.from_list(list_y)
        z = DynamicArray.from_list(list_z)
        empty = DynamicArray.empty()
        # Left identity: concat(empty, x) == x
        self.assertEqual(empty.concat(x), x)
        # Right identity: concat(x, empty) == x
        self.assertEqual(x.concat(empty), x)
        # Associativity: concat(concat(x, y), z) == concat(x, concat(y, z))
        self.assertEqual(x.concat(y).concat(z), x.concat(y.concat(z)))


if __name__ == '__main__':
    unittest.main()
