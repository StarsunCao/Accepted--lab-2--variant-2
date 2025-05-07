# Accepted - Lab 2 - Variant 2

This project implements an immutable dynamic array in Python
with a functional programming style.
The dynamic array supports operations such as adding elements,
removing elements, and various functional operations.
It maintains immutability by returning new instances for all operations
while efficiently reusing existing data structures.

---

## Project Structure

- `dynamic_array.py`
  Core implementation
  of the immutable DynamicArray class.
- `test_dynamic_array.py`
  Unit tests, Property-Based tests, and performance tests
  for the DynamicArray class.
- `README.md`
  Project documentation.

---

## Mutable vs Immutable Dynamic Array Implementation

### Lab 1 (Mutable)

- **Modifies existing data** in-place

- Methods like `add()`, `remove()`, and `map()` return `None`
  and change the original object

- Uses **imperative programming** with loops and direct array manipulation

### Lab 2 (Immutable)

- **Creates new instances** for every operation

- Methods like `cons()`, `remove()`, and `map()` return new `DynamicArray` objects

- Uses **functional programming** with recursion and immutable data structures

## Pros and Cons Comparison

| Aspect | Mutable (Lab 1) | Immutable (Lab 2) |
|----|----|-----|
| **Memory** | ✅ Reuses memory | ❌ More allocations |
| **Speed** | ✅ Faster updates | ❌ Copy overhead |
| **Threading** | ❌ Race conditions | ✅ Thread-safe |
| **Debug** | ❌ Hard to track | ✅ Stable state |
| **Reasoning** | ❌ Side effects | ✅ Predictable |
| **Code** | ✅ Simpler | ❌ More complex |
| **History** | ❌ No history | ✅ Enables undo |
| **References** | ❌ Shared changes | ✅ Isolated |
| **Stack** | ✅ No limits | ❌ Recursion limits |

---

## Features

- **PBT: `test_empty`**
  Tests the `empty` method to ensure it creates an empty dynamic array
  with the correct initial state.
- **PBT: `test_from_list`**
  Validates that creating a dynamic array from a list preserves all elements
  and maintains the correct order.
- **PBT: `test_cons`**
  Tests the `cons` operation to ensure elements are correctly added to the
  dynamic array and that resizing works as expected.
- **PBT: `test_remove`**
  Tests the `remove` method to confirm elements are correctly removed while
  maintaining immutability of the original array.
- **PBT: `test_length`**
  Verifies that the `length` method correctly reports the number of elements
  in the dynamic array.
- **PBT: `test_member`**
  Verifies that the `member` method correctly determines whether a given value
  exists in the dynamic array.
- **PBT: `test_reverse`**
  Tests the `reverse` method to ensure that the order of elements is correctly reversed
  while preserving the original array.
- **PBT: `test_to_list`**
  Confirms that converting a dynamic array back to a list preserves all elements
  and their order.
- **PBT: `test_get`**
  Tests the `get` method for retrieving elements at specific indices,
  including support for negative indices and boundary checking.
- **PBT: `test_set`**
  Validates the `set` method for updating elements at specific indices
  while maintaining immutability.
- **PBT: `test_filter`**
  Validates that `filter` correctly creates a new array with elements that satisfy
  the given predicate while maintaining immutability.
- **PBT: `test_map`**
  Ensures `map` applies a transformation function to all elements and
  returns a new array with the transformed values.
- **PBT: `test_reduce`**
  Confirms that `reduce` accumulates elements using a specified function and
  initial value, producing the correct result.
- **PBT: `test_iterator`**
  Verifies that the dynamic array supports iteration and that iterating over
  the structure produces the correct sequence of elements.
- **PBT: `test_intersection`**
  Tests the `intersection` method to ensure it correctly returns a new array
  containing only elements present in both arrays.
- **PBT: `test_concat`**
  Validates the `concat` method for combining two arrays while maintaining
  immutability of the original arrays.
- **PBT: `test_eq`**
  Tests the equality comparison to ensure arrays with the same elements
  are considered equal.
- **PBT: `test_str`**
  Verifies that the string representation of the array is correctly formatted.
- **PBT: `test_iter`**
  Tests the iteration protocol to ensure arrays can be iterated over correctly.
- **PBT: `test_none_values`**
  Ensures the dynamic array can store, retrieve, and process `None` values
  without errors.
- **PBT: `test_empty_operations`**
  Tests various operations on empty arrays to ensure they behave correctly.
- **PBT: `test_growth_factor_one`**
  Tests the resizing behavior when the growth factor is set to 1.0.
- **PBT: `test_monoid_laws`**
  Validates the Monoid properties (identity and associativity) for the
  dynamic array with respect to the `concat` operation.

---

## Contribution

- **Cao Xinyang**: initial version.
- **Xiong Shichi**: subsequent improvements.

---

## Changelog
- 07.05.2025 - 1  
   - Compare lab 1 and lab 2 implementation.
- 23.03.2025 - 0  
   - Initial implementation of immutable dynamic array
   - Added comprehensive test suite including unit tests and property-based tests
   - Implemented functional programming operations (map, filter, reduce)
   - Added support for Monoid interface with concat operation

---

## Design notes

- <https://en.wikipedia.org/wiki/Dynamic_array>
- <https://en.wikipedia.org/wiki/Persistent_data_structure>
- <https://en.wikipedia.org/wiki/Functional_programming>
