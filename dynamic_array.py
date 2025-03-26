from typing import Any, Callable, Generator, Tuple, TypeVar

T = TypeVar('T')
U = TypeVar('U')


class DynamicArray:
    """Immutable dynamic array implementation supporting
    functional programming style operations.

    Attributes:
        _data: Tuple storing the elements
        _length: Number of actual elements in the array
        _capacity: Capacity of the array
        _growth_factor: Growth factor for expansion, default 2.0
    """
    def __init__(self, data: Tuple[Any, ...], length: int, capacity: int,
                 growth_factor: float = 2.0):
        """Initialize dynamic array.
        Args:
            data: Tuple containing elements
            length: Number of elements in the array
            capacity: Array capacity
            growth_factor: Growth factor for expansion, default 2.0
        """
        self._data = data
        self._length = length
        self._capacity = capacity
        self._growth_factor = growth_factor

    @staticmethod
    def empty(growth_factor: float = 2.0) -> 'DynamicArray':
        """Create an empty dynamic array.
        Args:
            growth_factor: Growth factor for expansion, default 2.0
        Returns:
            New empty dynamic array
        """
        return DynamicArray((), 0, 0, growth_factor)

    @staticmethod
    def from_list(py_list: list, growth_factor: float = 2.0) -> 'DynamicArray':
        """Create dynamic array from Python list.
        Args:
            py_list: Python list
            growth_factor: Growth factor for expansion, default 2.0
        Returns:
            Dynamic array containing list elements
        """
        length = len(py_list)
        capacity = length
        data = tuple(py_list)
        return DynamicArray(data, length, capacity, growth_factor)

    def cons(self, element: Any) -> 'DynamicArray':
        """Add element to the front of the array.
        Args:
            element: Element to add
        Returns:
            New array with added element
        """
        if self._length >= self._capacity:
            # Need to resize
            return self._resize().cons(element)
        new_data = (element,) + self._data
        return DynamicArray(new_data, self._length + 1,
                            self._capacity, self._growth_factor)

    def _resize(self) -> 'DynamicArray':
        """Expand array capacity.
        Returns:
            Resized new array
        """
        # Fix for growth_factor=1 case, ensure at least 1 capacity increase
        new_capacity = max(1, int(self._capacity * self._growth_factor))
        # If new capacity equals current, increment by 1
        if new_capacity <= self._capacity:
            new_capacity = self._capacity + 1
        new_data = self._data + (None,) * (new_capacity - self._capacity)
        return DynamicArray(new_data, self._length,
                            new_capacity, self._growth_factor)

    def remove(self, value: Any) -> 'DynamicArray':
        """Remove first occurrence of value.
        Args:
            value: Value to remove
        Returns:
            New array with value removed
        """
        def _remove_rec(idx: int, acc: Tuple) -> Tuple:
            if idx >= self._length:
                return acc
            current = self._data[idx]
            if current == value and len(acc) == idx:
                return acc + self._data[idx + 1:self._length]
            return _remove_rec(idx + 1, acc + (current,))
        result = _remove_rec(0, ())
        return DynamicArray(result + (None,) * (self._capacity - len(result)),
                            len(result), self._capacity, self._growth_factor)

    def length(self) -> int:
        """Get array length.
        Returns:
            Number of elements in array
        """
        return self._length

    def member(self, value: Any) -> bool:
        """Check if value exists in array.
        Args:
            value: Value to check
        Returns:
            True if value exists, else False
        """
        def _member_rec(idx: int) -> bool:
            if idx >= self._length:
                return False
            if self._data[idx] == value:
                return True
            return _member_rec(idx + 1)
        return _member_rec(0)

    def reverse(self) -> 'DynamicArray':
        """Create reversed array.
        Returns:
            New reversed array
        """
        def _reverse_rec(idx: int, acc: Tuple) -> Tuple:
            if idx < 0:
                return acc
            return _reverse_rec(idx - 1, acc + (self._data[idx],))
        reversed_data = _reverse_rec(self._length - 1, ())
        return DynamicArray(reversed_data +
                            (None,) * (self._capacity - self._length),
                            self._length, self._capacity, self._growth_factor)

    def to_list(self) -> list:
        """Convert to Python list.
        Returns:
            Python list containing array elements
        """
        return list(self._data[:self._length])

    def get(self, index: int) -> Any:
        """Get element at specified index.
        Args:
            index: Index (supports negative indexing)
        Returns:
            Element at index
        Raises:
            IndexError: If index out of bounds
        """
        adjusted_index = index if index >= 0 else self._length + index
        if adjusted_index < 0 or adjusted_index >= self._length:
            raise IndexError("Index out of range")
        return self._data[adjusted_index]

    def set(self, index: int, value: Any) -> 'DynamicArray':
        """Set element at specified index.
        Args:
            index: Index (supports negative indexing)
            value: New value
        Returns:
            New updated array
        Raises:
            IndexError: If index out of bounds
        """
        adjusted_index = index if index >= 0 else self._length + index
        if adjusted_index < 0 or adjusted_index >= self._length:
            raise IndexError("Index out of range")

        def _set_rec(idx: int, acc: Tuple) -> Tuple:
            if idx >= self._length:
                return acc
            current = value if idx == adjusted_index else self._data[idx]
            return _set_rec(idx + 1, acc + (current,))
        new_data = _set_rec(0, ())
        return DynamicArray(new_data + self._data[self._length:],
                            self._length, self._capacity, self._growth_factor)

    def filter(self, predicate: Callable[[Any], bool]) -> 'DynamicArray':
        """Filter array elements.
        Args:
            predicate: Function returning True for elements to keep
        Returns:
            New filtered array
        """
        def _filter_rec(idx: int, acc: Tuple) -> Tuple:
            if idx >= self._length:
                return acc
            current = self._data[idx]
            if predicate(current):
                return _filter_rec(idx + 1, acc + (current,))
            return _filter_rec(idx + 1, acc)
        filtered_data = _filter_rec(0, ())
        return DynamicArray(filtered_data +
                            (None,) * (self._capacity - len(filtered_data)),
                            len(filtered_data),
                            self._capacity, self._growth_factor)

    def map(self, func: Callable[[Any], Any]) -> 'DynamicArray':
        """Map function over array elements.
        Args:
            func: Function to apply to each element
        Returns:
            New mapped array
        """
        def _map_rec(idx: int, acc: Tuple) -> Tuple:
            if idx >= self._length:
                return acc
            return _map_rec(idx + 1, acc + (func(self._data[idx]),))
        mapped_data = _map_rec(0, ())
        return DynamicArray(mapped_data +
                            (None,) * (self._capacity - self._length),
                            self._length, self._capacity, self._growth_factor)

    def reduce(self, func: Callable[[Any, Any], Any], initial: Any) -> Any:
        """Reduce array elements.
        Args:
            func: Reduction function taking accumulator and current element
            initial: Initial accumulator value
        Returns:
            Reduction result
        """
        def _reduce_rec(idx: int, acc: Any) -> Any:
            if idx >= self._length:
                return acc
            return _reduce_rec(idx + 1, func(acc, self._data[idx]))
        return _reduce_rec(0, initial)

    def iterator(self) -> Generator[Any, None, None]:
        """Get array iterator.
        Returns:
            Generator yielding array elements
        """
        for i in range(self._length):
            yield self._data[i]

    def intersection(self, other: 'DynamicArray') -> 'DynamicArray':
        """Get intersection with another array.
        Args:
            other: Another dynamic array
        Returns:
            New array containing common elements
        """
        def _intersection_rec(idx: int, acc: Tuple) -> Tuple:
            if idx >= self._length:
                return acc
            current = self._data[idx]
            if other.member(current):
                return _intersection_rec(idx + 1, acc + (current,))
            return _intersection_rec(idx + 1, acc)
        intersect_data = _intersection_rec(0, ())
        return DynamicArray(intersect_data +
                            (None,) * (self._capacity - len(intersect_data)),
                            len(intersect_data),
                            self._capacity, self._growth_factor)

    def concat(self, other: 'DynamicArray') -> 'DynamicArray':
        """Concatenate two arrays.
        Args:
            other: Array to concatenate
        Returns:
            New concatenated array
        """
        total_length = self._length + other._length
        new_capacity = max(self._capacity, total_length)
        # Expand if needed
        if new_capacity < total_length:
            new_capacity = max(1, int(new_capacity * self._growth_factor))
        new_data = self._data[:self._length] + other._data[:other._length]
        if len(new_data) < new_capacity:
            new_data = new_data + (None,) * (new_capacity - len(new_data))
        return DynamicArray(new_data, total_length, new_capacity,
                            self._growth_factor)

    def __eq__(self, other: object) -> bool:
        """Check array equality.
        Args:
            other: Object to compare
        Returns:
            True if arrays have same content, else False
        """
        if not isinstance(other, DynamicArray):
            return False
        if self._length != other._length:
            return False

        def _eq_rec(idx: int) -> bool:
            if idx >= self._length:
                return True
            if self._data[idx] != other._data[idx]:
                return False
            return _eq_rec(idx + 1)
        return _eq_rec(0)

    def __str__(self) -> str:
        """String representation.
        Returns:
            String in format [None, 1, 3]
        """
        return str(list(self._data[:self._length]))

    def __iter__(self) -> Generator[Any, None, None]:
        """Implement iteration protocol.
        Returns:
            Array iterator
        """
        return self.iterator()
