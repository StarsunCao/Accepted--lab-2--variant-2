import unittest
from typing import Any, List, Callable

from hypothesis import given, strategies as st

from dynamic_array import DynamicArray


class TestDynamicArray(unittest.TestCase):
    """测试DynamicArray类的功能。"""

    def test_empty(self):
        """测试创建空数组。"""
        arr = DynamicArray.empty()
        self.assertEqual(arr.length(), 0)
        self.assertEqual(str(arr), "[]")

    def test_from_list(self):
        """测试从列表创建数组。"""
        arr = DynamicArray.from_list([1, 2, 3])
        self.assertEqual(arr.length(), 3)
        self.assertEqual(str(arr), "[1, 2, 3]")

    def test_cons(self):
        """测试cons操作。"""
        arr = DynamicArray.empty()
        arr = arr.cons(3).cons(2).cons(1)
        self.assertEqual(arr.length(), 3)
        self.assertEqual(str(arr), "[1, 2, 3]")

    def test_remove(self):
        """测试remove操作。"""
        arr = DynamicArray.from_list([1, 2, 3, 2])
        arr = arr.remove(2)
        self.assertEqual(str(arr), "[1, 3, 2]")

        # 测试移除不存在的元素
        arr = arr.remove(4)
        self.assertEqual(str(arr), "[1, 3, 2]")

    def test_length(self):
        """测试length操作。"""
        arr = DynamicArray.from_list([1, 2, 3])
        self.assertEqual(arr.length(), 3)

        arr = arr.cons(0)
        self.assertEqual(arr.length(), 4)

    def test_member(self):
        """测试member操作。"""
        arr = DynamicArray.from_list([1, 2, 3])
        self.assertTrue(arr.member(1))
        self.assertTrue(arr.member(2))
        self.assertTrue(arr.member(3))
        self.assertFalse(arr.member(4))

    def test_reverse(self):
        """测试reverse操作。"""
        arr = DynamicArray.from_list([1, 2, 3])
        reversed_arr = arr.reverse()
        self.assertEqual(str(reversed_arr), "[3, 2, 1]")

        # 原数组不变
        self.assertEqual(str(arr), "[1, 2, 3]")

    def test_to_list(self):
        """测试to_list操作。"""
        arr = DynamicArray.from_list([1, 2, 3])
        self.assertEqual(arr.to_list(), [1, 2, 3])

    def test_get(self):
        """测试get操作。"""
        arr = DynamicArray.from_list([1, 2, 3])
        self.assertEqual(arr.get(0), 1)
        self.assertEqual(arr.get(1), 2)
        self.assertEqual(arr.get(2), 3)

        # 测试负索引
        self.assertEqual(arr.get(-1), 3)
        self.assertEqual(arr.get(-2), 2)
        self.assertEqual(arr.get(-3), 1)

        # 测试索引越界
        with self.assertRaises(IndexError):
            arr.get(3)
        with self.assertRaises(IndexError):
            arr.get(-4)

    def test_set(self):
        """测试set操作。"""
        arr = DynamicArray.from_list([1, 2, 3])
        new_arr = arr.set(1, 5)

        # 新数组已更新
        self.assertEqual(str(new_arr), "[1, 5, 3]")

        # 原数组不变
        self.assertEqual(str(arr), "[1, 2, 3]")

        # 测试负索引
        new_arr = arr.set(-1, 6)
        self.assertEqual(str(new_arr), "[1, 2, 6]")

        # 测试索引越界
        with self.assertRaises(IndexError):
            arr.set(3, 7)
        with self.assertRaises(IndexError):
            arr.set(-4, 7)

    def test_filter(self):
        """测试filter操作。"""
        arr = DynamicArray.from_list([1, 2, 3, 4, 5])
        filtered = arr.filter(lambda x: x % 2 == 0)
        self.assertEqual(str(filtered), "[2, 4]")

        # 原数组不变
        self.assertEqual(str(arr), "[1, 2, 3, 4, 5]")

    def test_map(self):
        """测试map操作。"""
        arr = DynamicArray.from_list([1, 2, 3])
        mapped = arr.map(lambda x: x * 2)
        self.assertEqual(str(mapped), "[2, 4, 6]")

        # 原数组不变
        self.assertEqual(str(arr), "[1, 2, 3]")

    def test_reduce(self):
        """测试reduce操作。"""
        arr = DynamicArray.from_list([1, 2, 3, 4])
        sum_result = arr.reduce(lambda acc, x: acc + x, 0)
        self.assertEqual(sum_result, 10)

        product_result = arr.reduce(lambda acc, x: acc * x, 1)
        self.assertEqual(product_result, 24)

    def test_iterator(self):
        """测试iterator操作。"""
        arr = DynamicArray.from_list([1, 2, 3])
        iterator = arr.iterator()
        self.assertEqual(next(iterator), 1)
        self.assertEqual(next(iterator), 2)
        self.assertEqual(next(iterator), 3)
        with self.assertRaises(StopIteration):
            next(iterator)

    def test_intersection(self):
        """测试intersection操作。"""
        arr1 = DynamicArray.from_list([1, 2, 3, 4])
        arr2 = DynamicArray.from_list([3, 4, 5, 6])

        intersection = arr1.intersection(arr2)
        self.assertEqual(str(intersection), "[3, 4]")

        # 原数组不变
        self.assertEqual(str(arr1), "[1, 2, 3, 4]")
        self.assertEqual(str(arr2), "[3, 4, 5, 6]")

    def test_concat(self):
        """测试concat操作。"""
        arr1 = DynamicArray.from_list([1, 2])
        arr2 = DynamicArray.from_list([3, 4])

        concatenated = arr1.concat(arr2)
        self.assertEqual(str(concatenated), "[1, 2, 3, 4]")

        # 原数组不变
        self.assertEqual(str(arr1), "[1, 2]")
        self.assertEqual(str(arr2), "[3, 4]")

    def test_eq(self):
        """测试__eq__操作。"""
        arr1 = DynamicArray.from_list([1, 2, 3])
        arr2 = DynamicArray.from_list([1, 2, 3])
        arr3 = DynamicArray.from_list([1, 2, 4])

        self.assertEqual(arr1, arr2)
        self.assertNotEqual(arr1, arr3)
        self.assertNotEqual(arr1, "not an array")

    def test_str(self):
        """测试__str__操作。"""
        arr = DynamicArray.from_list([1, None, 3])
        self.assertEqual(str(arr), "[1, None, 3]")

    def test_iter(self):
        """测试__iter__操作。"""
        arr = DynamicArray.from_list([1, 2, 3])
        items = []
        for item in arr:
            items.append(item)

        self.assertEqual(items, [1, 2, 3])

    def test_none_values(self):
        """测试None值处理。"""
        arr = DynamicArray.from_list([None, 1, None, 3])
        self.assertEqual(arr.length(), 4)
        self.assertEqual(str(arr), "[None, 1, None, 3]")

        # 测试None值的成员检查
        self.assertTrue(arr.member(None))

        # 测试移除None值
        arr_without_none = arr.remove(None)
        self.assertEqual(str(arr_without_none), "[1, None, 3]")

    def test_empty_operations(self):
        """测试空数组的操作。"""
        empty_arr = DynamicArray.empty()

        # 测试空数组的基本操作
        self.assertEqual(empty_arr.length(), 0)
        self.assertFalse(empty_arr.member(1))
        self.assertEqual(empty_arr.to_list(), [])

        # 测试空数组的reverse
        self.assertEqual(empty_arr.reverse().to_list(), [])

        # 测试空数组的filter和map
        self.assertEqual(empty_arr.filter(lambda x: True).to_list(), [])
        self.assertEqual(empty_arr.map(lambda x: x * 2).to_list(), [])

        # 测试空数组的reduce
        self.assertEqual(empty_arr.reduce(lambda acc, x: acc + x, 0), 0)

        # 测试空数组的concat
        arr = DynamicArray.from_list([1, 2])
        self.assertEqual(empty_arr.concat(arr).to_list(), [1, 2])
        self.assertEqual(arr.concat(empty_arr).to_list(), [1, 2])

    def test_growth_factor_one(self):
        """测试growth_factor=1时的扩容行为。"""
        arr = DynamicArray.empty(growth_factor=1.0)

        # 连续添加元素，观察扩容行为
        for i in range(5):
            arr = arr.cons(i)

        self.assertEqual(arr.length(), 5)
        self.assertEqual(arr.to_list(), [4, 3, 2, 1, 0])

    def test_api(self):
        """用户提供的API测试。"""
        # 创建空数组
        empty_array = DynamicArray.empty()
        self.assertEqual(empty_array.length(), 0)

        # 从列表创建数组
        array_from_list = DynamicArray.from_list([1, 2, 3])
        self.assertEqual(array_from_list.length(), 3)

        # 添加元素
        new_array = array_from_list.cons(0)
        self.assertEqual(new_array.length(), 4)
        self.assertEqual(new_array.get(0), 0)

        # 移除元素
        array_without_2 = array_from_list.remove(2)
        self.assertEqual(array_without_2.length(), 2)
        self.assertEqual(array_without_2.to_list(), [1, 3])

        # 检查成员
        self.assertTrue(array_from_list.member(2))
        self.assertFalse(array_from_list.member(4))

        # 反转数组
        reversed_array = array_from_list.reverse()
        self.assertEqual(reversed_array.to_list(), [3, 2, 1])

        # 设置元素
        modified_array = array_from_list.set(1, 5)
        self.assertEqual(modified_array.to_list(), [1, 5, 3])

        # 过滤元素
        filtered_array = array_from_list.filter(lambda x: x > 1)
        self.assertEqual(filtered_array.to_list(), [2, 3])

        # 映射元素
        mapped_array = array_from_list.map(lambda x: x * 2)
        self.assertEqual(mapped_array.to_list(), [2, 4, 6])

        # 归约元素
        sum_result = array_from_list.reduce(lambda acc, x: acc + x, 0)
        self.assertEqual(sum_result, 6)

        # 数组交集
        array1 = DynamicArray.from_list([1, 2, 3])
        array2 = DynamicArray.from_list([2, 3, 4])
        intersection_array = array1.intersection(array2)
        self.assertEqual(intersection_array.to_list(), [2, 3])

        # 数组连接
        concatenated_array = array1.concat(array2)
        self.assertEqual(concatenated_array.to_list(), [1, 2, 3, 2, 3, 4])


class MonoidLawsTest(unittest.TestCase):
    """测试Monoid定律。"""

    @given(st.lists(st.integers()), st.lists(st.integers()), st.lists(st.integers()))
    def test_monoid_laws(self, list_x, list_y, list_z):
        """使用Hypothesis测试Monoid定律。"""
        x = DynamicArray.from_list(list_x)
        y = DynamicArray.from_list(list_y)
        z = DynamicArray.from_list(list_z)
        empty = DynamicArray.empty()

        # 左单位元: concat(empty, x) == x
        self.assertEqual(empty.concat(x), x)

        # 右单位元: concat(x, empty) == x
        self.assertEqual(x.concat(empty), x)

        # 结合律: concat(concat(x, y), z) == concat(x, concat(y, z))
        self.assertEqual(x.concat(y).concat(z), x.concat(y.concat(z)))

if __name__ == '__main__':
    unittest.main()