# dynamic_array.py
from functools import reduce as _reduce
from typing import Any, Callable, Generator, Iterable, Optional, Tuple, Union


class DynamicArray:
    def __init__(
            self,
            data: Optional[Tuple[Any, ...]] = None,
            capacity: int = 0,
            length: int = 0,
            growth_factor: float = 2.0
    ):
        self._data = data or tuple()
        self._capacity = max(capacity, len(self._data))
        self._length = length if 0 <= length <= self._capacity else 0
        self.growth_factor = max(1.0, growth_factor)

    @property
    def capacity(self) -> int:
        return self._capacity

    @property
    def length(self) -> int:
        return self._length

    def is_empty(self) -> bool:
        return self._length == 0

    def _resize(self, min_capacity: int) -> 'DynamicArray':
        new_capacity = max(min_capacity, int(self.capacity * self.growth_factor))
        new_data = self._data + (None,) * (new_capacity - self.capacity)
        return DynamicArray(new_data, new_capacity, self.length, self.growth_factor)

    def cons(self, element: Any) -> 'DynamicArray':
        if self.length == self.capacity:
            new_arr = self._resize(self.capacity + 1)
        else:
            new_arr = DynamicArray(
                self._data, self.capacity, self.length, self.growth_factor
            )

        new_data = list(new_arr._data)
        new_data[new_arr.length] = element
        return DynamicArray(
            tuple(new_data),
            new_arr.capacity,
            new_arr.length + 1,
            self.growth_factor
        )

    def get(self, index: int) -> Any:
        if index < 0:
            index += self.length
        if not 0 <= index < self.length:
            raise IndexError("Index out of bounds")
        return self._data[index]

    def set(self, index: int, value: Any) -> 'DynamicArray':
        if index < 0:
            index += self.length
        if not 0 <= index < self.length:
            raise IndexError("Index out of bounds")

        new_data = list(self._data)
        new_data[index] = value
        return DynamicArray(
            tuple(new_data), self.capacity, self.length, self.growth_factor
        )

    def remove(self, value: Any) -> 'DynamicArray':
        def _remove_recursive(
                data: Tuple[Any, ...], idx: int, new_data: list, removed: bool
        ) -> Tuple[Tuple[Any, ...], int]:
            if idx >= self.length:
                return tuple(new_data), self.length - (1 if removed else 0)

            if not removed and data[idx] == value:
                return _remove_recursive(data, idx + 1, new_data, True)

            new_data.append(data[idx])
            return _remove_recursive(data, idx + 1, new_data, removed)

        new_data, new_length = _remove_recursive(self._data, 0, [], False)
        return DynamicArray(new_data, self.capacity, new_length, self.growth_factor)

    def member(self, value: Any) -> bool:
        def _member_recursive(idx: int) -> bool:
            if idx >= self.length:
                return False
            return self._data[idx] == value or _member_recursive(idx + 1)

        return _member_recursive(0)

    def reverse(self) -> 'DynamicArray':
        def _reverse_recursive(
                src_idx: int, dst_idx: int, new_data: list
        ) -> 'DynamicArray':
            if src_idx < 0:
                return DynamicArray(
                    tuple(new_data), self.capacity, self.length, self.growth_factor
                )
            new_data[dst_idx] = self._data[src_idx]
            return _reverse_recursive(src_idx - 1, dst_idx + 1, new_data)

        new_data = [None] * self.capacity
        return _reverse_recursive(self.length - 1, 0, new_data)

    def filter(self, predicate: Callable[[Any], bool]) -> 'DynamicArray':
        def _filter_recursive(
                idx: int, new_data: list, new_length: int
        ) -> Tuple[Tuple[Any, ...], int]:
            if idx >= self.length:
                return tuple(new_data), new_length

            if predicate(self._data[idx]):
                new_data.append(self._data[idx])
                return _filter_recursive(idx + 1, new_data, new_length + 1)
            return _filter_recursive(idx + 1, new_data, new_length)

        filtered_data, new_length = _filter_recursive(0, [], 0)
        return DynamicArray(filtered_data, new_length, new_length, self.growth_factor)

    def map(self, func: Callable[[Any], Any]) -> 'DynamicArray':
        def _map_recursive(
                idx: int, new_data: list, new_length: int
        ) -> 'DynamicArray':
            if idx >= self.length:
                return DynamicArray(
                    tuple(new_data), self.capacity, new_length, self.growth_factor
                )

            new_data.append(func(self._data[idx]))
            return _map_recursive(idx + 1, new_data, new_length + 1)

        return _map_recursive(0, [], 0)

    def reduce(self, func: Callable[[Any, Any], Any], initial: Any) -> Any:
        def _reduce_recursive(idx: int, acc: Any) -> Any:
            if idx >= self.length:
                return acc
            return _reduce_recursive(idx + 1, func(acc, self._data[idx]))

        return _reduce_recursive(0, initial)

    def intersection(self, other: 'DynamicArray') -> 'DynamicArray':
        def _intersect_recursive(
                idx: int, new_data: list, seen: set
        ) -> 'DynamicArray':
            if idx >= self.length:
                return DynamicArray(
                    tuple(new_data), len(new_data), len(new_data), self.growth_factor
                )

            elem = self._data[idx]
            if elem in seen and elem not in new_data:
                new_data.append(elem)
            return _intersect_recursive(idx + 1, new_data, seen)

        other_elements = {other.get(i) for i in range(other.length)}
        return _intersect_recursive(0, [], other_elements)

    def concat(self, other: 'DynamicArray') -> 'DynamicArray':
        def _concat_recursive(
                idx: int, new_data: list, total_length: int
        ) -> 'DynamicArray':
            if idx >= total_length:
                growth_factor = max(self.growth_factor, other.growth_factor)
                return DynamicArray(
                    tuple(new_data), len(new_data), total_length, growth_factor
                )

            elem = self._data[idx] if idx < self.length else other._data[idx - self.length]
            new_data.append(elem)
            return _concat_recursive(idx + 1, new_data, total_length)

        total_length = self.length + other.length
        return _concat_recursive(0, [], total_length)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, DynamicArray):
            return False
        return self._data[:self.length] == other._data[:other.length]

    def __str__(self) -> str:
        elements = [str(self._data[i]) for i in range(self.length)]
        return f"[{', '.join(elements)}]"

    def __iter__(self) -> Generator[Any, None, None]:
        def _iter_recursive(idx: int):
            if idx < self.length:
                yield self._data[idx]
                yield from _iter_recursive(idx + 1)

        return _iter_recursive(0)


# Factory functions
def empty(growth_factor: float = 2.0) -> DynamicArray:
    return DynamicArray(growth_factor=growth_factor)


def from_list(py_list: list, growth_factor: float = 2.0) -> DynamicArray:
    capacity = max(len(py_list), 1)
    return DynamicArray(
        tuple(py_list + [None] * (capacity - len(py_list))),
        capacity,
        len(py_list),
        growth_factor
    )


def cons(element: Any, arr: DynamicArray) -> DynamicArray:
    return arr.cons(element)


def remove(arr: DynamicArray, value: Any) -> DynamicArray:
    return arr.remove(value)


def length(arr: DynamicArray) -> int:
    return arr.length


def member(arr: DynamicArray, value: Any) -> bool:
    return arr.member(value)


def reverse(arr: DynamicArray) -> DynamicArray:
    return arr.reverse()


def to_list(arr: DynamicArray) -> list:
    return [arr.get(i) for i in range(arr.length)]


def concat(arr1: DynamicArray, arr2: DynamicArray) -> DynamicArray:
    return arr1.concat(arr2)


def filter(arr: DynamicArray, predicate: Callable[[Any], bool]) -> DynamicArray:
    return arr.filter(predicate)


def map(arr: DynamicArray, func: Callable[[Any], Any]) -> DynamicArray:  # noqa: A001
    return arr.map(func)


def reduce(arr: DynamicArray, func: Callable[[Any, Any], Any], initial: Any) -> Any:
    return arr.reduce(func, initial)


def iterator(arr: DynamicArray) -> Generator[Any, None, None]:
    return iter(arr)


def intersection(arr1: DynamicArray, arr2: DynamicArray) -> DynamicArray:
    return arr1.intersection(arr2)