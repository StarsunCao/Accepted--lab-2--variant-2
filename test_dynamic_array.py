# test_dynamic_array.py
import pytest
from hypothesis import given, strategies as st
from dynamic_array import (
    DynamicArray,
    cons,
    empty,
    from_list,
    length,
    member,
    remove,
    reverse,
    to_list,
    concat,
    filter,
    map,
    reduce,
    intersection,
)


# Original API test
def test_api():
    empty_arr = empty()
    l1 = cons(None, cons(1, empty()))
    l2 = cons(1, cons(None, empty()))

    assert str(empty_arr) == "[]"
    assert str(l1) == "[None, 1]"
    assert str(l2) == "[1, None]"
    assert empty_arr != l1
    assert empty_arr != l2
    assert l1 != l2
    assert l1 == cons(None, cons(1, empty()))

    assert length(empty_arr) == 0
    assert length(l1) == 2
    assert length(l2) == 2

    assert str(remove(l1, None)) == "[1]"
    assert str(remove(l1, 1)) == "[None]"

    assert not member(None, empty_arr)
    assert member(None, l1)
    assert member(1, l1)
    assert not member(2, l1)

    assert l1 == reverse(l2)

    assert to_list(l1) == [None, 1]
    assert l1 == from_list([None, 1])

    assert concat(l1, l2) == from_list([None, 1, 1, None])

    buf = []
    for e in l1:
        buf.append(e)
    assert buf == [None, 1]

    lst = to_list(l1) + to_list(l2)
    for e in l1:
        lst.remove(e)
    for e in l2:
        lst.remove(e)
    assert lst == []


# Property-based tests
@given(st.lists(st.integers() | st.none()))
def test_from_list_to_list_roundtrip(lst):
    arr = from_list(lst)
    assert to_list(arr) == lst


@given(st.lists(st.integers()), st.integers())
def test_cons_property(lst, elem):
    arr = from_list(lst)
    new_arr = cons(elem, arr)
    assert to_list(new_arr) == [elem] + lst


@given(st.lists(st.integers()), st.integers())
def test_member_property(lst, elem):
    arr = from_list(lst)
    assert member(arr, elem) == (elem in lst)


@given(st.lists(st.integers()))
def test_reverse_property(lst):
    arr = from_list(lst)
    assert to_list(reverse(arr)) == list(reversed(lst))


@given(st.lists(st.integers()), st.lists(st.integers()))
def test_concat_property(lst1, lst2):
    arr1 = from_list(lst1)
    arr2 = from_list(lst2)
    assert to_list(concat(arr1, arr2)) == lst1 + lst2


# Monoid laws tests
def test_monoid_identity():
    arr = from_list([1, 2, 3])
    empty_arr = empty()

    assert concat(empty_arr, arr) == arr
    assert concat(arr, empty_arr) == arr


@given(st.lists(st.integers()), st.lists(st.integers()), st.lists(st.integers()))
def test_monoid_associativity(lst1, lst2, lst3):
    arr1 = from_list(lst1)
    arr2 = from_list(lst2)
    arr3 = from_list(lst3)

    left_assoc = concat(concat(arr1, arr2), arr3)
    right_assoc = concat(arr1, concat(arr2, arr3))
    assert left_assoc == right_assoc


# Edge cases tests
def test_none_handling():
    arr = cons(None, cons(0, empty()))
    assert member(arr, None)
    assert to_list(remove(arr, None)) == [0]


def test_empty_operations():
    arr = empty()
    assert length(arr) == 0
    assert not member(arr, 0)
    assert to_list(arr) == []
    assert str(arr) == "[]"


def test_negative_indices():
    arr = from_list([1, 2, 3])
    assert arr.get(-1) == 3
    assert arr.get(-3) == 1


# Additional functional tests
def test_filter_map_reduce():
    arr = from_list([1, 2, 3, 4])

    filtered = filter(arr, lambda x: x % 2 == 0)
    assert to_list(filtered) == [2, 4]

    mapped = map(arr, lambda x: x * 2)
    assert to_list(mapped) == [2, 4, 6, 8]

    reduced = reduce(arr, lambda acc, x: acc + x, 0)
    assert reduced == 10


def test_intersection():
    arr1 = from_list([1, 2, 3, 4])
    arr2 = from_list([3, 4, 5, 6])
    assert to_list(intersection(arr1, arr2)) == [3, 4]