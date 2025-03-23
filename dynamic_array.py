from typing import Any, Callable, Generator, Tuple, TypeVar

T = TypeVar('T')
U = TypeVar('U')


class DynamicArray:
    """不可变动态数组实现，支持函数式编程风格操作。

    属性:
        _data: 存储元素的不可变元组
        _length: 数组中实际元素的数量
        _capacity: 数组的容量
        _growth_factor: 扩容因子，默认为2
    """

    def __init__(self, data: Tuple[Any, ...], length: int, capacity: int,
                 growth_factor: float = 2.0):
        """初始化动态数组。

        Args:
            data: 存储元素的元组
            length: 数组中实际元素的数量
            capacity: 数组的容量
            growth_factor: 扩容因子，默认为2.0
        """
        self._data = data
        self._length = length
        self._capacity = capacity
        self._growth_factor = growth_factor

    @staticmethod
    def empty(growth_factor: float = 2.0) -> 'DynamicArray':
        """创建一个空的动态数组。

        Args:
            growth_factor: 扩容因子，默认为2.0

        Returns:
            一个新的空动态数组
        """
        return DynamicArray((), 0, 0, growth_factor)

    @staticmethod
    def from_list(py_list: list, growth_factor: float = 2.0) -> 'DynamicArray':
        """从Python列表创建动态数组。

        Args:
            py_list: Python列表
            growth_factor: 扩容因子，默认为2.0

        Returns:
            包含列表元素的动态数组
        """
        length = len(py_list)
        capacity = length
        data = tuple(py_list)
        return DynamicArray(data, length, capacity, growth_factor)

    def cons(self, element: Any) -> 'DynamicArray':
        """在数组前端添加一个元素。

        Args:
            element: 要添加的元素

        Returns:
            包含新元素的新数组
        """
        if self._length >= self._capacity:
            # 需要扩容
            return self._resize().cons(element)

        new_data = (element,) + self._data
        return DynamicArray(new_data, self._length + 1,
                            self._capacity, self._growth_factor)

    def _resize(self) -> 'DynamicArray':
        """扩容数组。

        Returns:
            扩容后的新数组
        """
        # 修复当growth_factor为1时的问题，确保至少增加1个容量
        new_capacity = max(1, int(self._capacity * self._growth_factor))
        # 如果新容量等于当前容量，则至少增加1
        if new_capacity <= self._capacity:
            new_capacity = self._capacity + 1

        new_data = self._data + (None,) * (new_capacity - self._capacity)
        return DynamicArray(new_data, self._length,
                            new_capacity, self._growth_factor)

    def remove(self, value: Any) -> 'DynamicArray':
        """移除数组中的指定值（第一次出现）。

        Args:
            value: 要移除的值

        Returns:
            移除值后的新数组
        """

        def _remove_rec(idx: int, acc: Tuple) -> Tuple:
            if idx >= self._length:
                return acc

            current = self._data[idx]
            if current == value and len(acc) == idx:  # 只移除第一次出现
                return acc + self._data[idx + 1:self._length]

            return _remove_rec(idx + 1, acc + (current,))

        result = _remove_rec(0, ())
        return DynamicArray(result + (None,) * (self._capacity - len(result)),
                            len(result), self._capacity, self._growth_factor)

    def length(self) -> int:
        """返回数组的长度。

        Returns:
            数组中元素的数量
        """
        return self._length

    def member(self, value: Any) -> bool:
        """检查值是否在数组中。

        Args:
            value: 要检查的值

        Returns:
            如果值在数组中则为True，否则为False
        """

        def _member_rec(idx: int) -> bool:
            if idx >= self._length:
                return False
            if self._data[idx] == value:
                return True
            return _member_rec(idx + 1)

        return _member_rec(0)

    def reverse(self) -> 'DynamicArray':
        """返回反转后的数组。

        Returns:
            反转后的新数组
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
        """将动态数组转换为Python列表。

        Returns:
            包含数组元素的Python列表
        """
        return list(self._data[:self._length])

    def get(self, index: int) -> Any:
        """获取指定索引的元素。

        Args:
            index: 元素的索引，支持负索引

        Returns:
            索引位置的元素

        Raises:
            IndexError: 如果索引超出范围
        """
        adjusted_index = index if index >= 0 else self._length + index

        if adjusted_index < 0 or adjusted_index >= self._length:
            raise IndexError("索引超出范围")

        return self._data[adjusted_index]

    def set(self, index: int, value: Any) -> 'DynamicArray':
        """设置指定索引的元素值。

        Args:
            index: 元素的索引，支持负索引
            value: 新值

        Returns:
            更新后的新数组

        Raises:
            IndexError: 如果索引超出范围
        """
        adjusted_index = index if index >= 0 else self._length + index

        if adjusted_index < 0 or adjusted_index >= self._length:
            raise IndexError("索引超出范围")

        def _set_rec(idx: int, acc: Tuple) -> Tuple:
            if idx >= self._length:
                return acc

            current = value if idx == adjusted_index else self._data[idx]
            return _set_rec(idx + 1, acc + (current,))

        new_data = _set_rec(0, ())
        return DynamicArray(new_data + self._data[self._length:],
                            self._length, self._capacity, self._growth_factor)

    def filter(self, predicate: Callable[[Any], bool]) -> 'DynamicArray':
        """过滤数组元素。

        Args:
            predicate: 判断函数，返回True的元素将被保留

        Returns:
            过滤后的新数组
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
        """映射数组元素。

        Args:
            func: 映射函数，应用于每个元素

        Returns:
            映射后的新数组
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
        """归约数组元素。

        Args:
            func: 归约函数，接受累积值和当前元素
            initial: 初始累积值

        Returns:
            归约结果
        """

        def _reduce_rec(idx: int, acc: Any) -> Any:
            if idx >= self._length:
                return acc

            return _reduce_rec(idx + 1, func(acc, self._data[idx]))

        return _reduce_rec(0, initial)

    def iterator(self) -> Generator[Any, None, None]:
        """返回数组的迭代器。

        Returns:
            生成数组元素的生成器
        """
        for i in range(self._length):
            yield self._data[i]

    def intersection(self, other: 'DynamicArray') -> 'DynamicArray':
        """返回与另一个数组的交集。

        Args:
            other: 另一个动态数组

        Returns:
            包含两个数组共有元素的新数组
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
        """连接两个数组。

        Args:
            other: 要连接的另一个数组

        Returns:
            连接后的新数组
        """
        total_length = self._length + other._length
        new_capacity = max(self._capacity, total_length)

        # 如果容量不足，需要扩容
        if new_capacity < total_length:
            new_capacity = max(1, int(new_capacity * self._growth_factor))

        new_data = self._data[:self._length] + other._data[:other._length]
        if len(new_data) < new_capacity:
            new_data = new_data + (None,) * (new_capacity - len(new_data))

        return DynamicArray(new_data, total_length, new_capacity,
                            self._growth_factor)

    def __eq__(self, other: object) -> bool:
        """比较两个数组是否相等。

        Args:
            other: 要比较的对象

        Returns:
            如果两个数组内容相等则为True，否则为False
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
        """返回数组的字符串表示。

        Returns:
            数组的字符串表示，格式如 [None, 1, 3]
        """
        return str(list(self._data[:self._length]))

    def __iter__(self) -> Generator[Any, None, None]:
        """实现迭代协议。

        Returns:
            数组的迭代器
        """
        return self.iterator()
