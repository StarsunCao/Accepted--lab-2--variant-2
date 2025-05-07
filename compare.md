# Mutable vs Immutable Dynamic Array Implementation

## Core Implementation Approaches

### Lab 1 (Mutable)

* **Modifies existing data** in-place

* Methods like `add()`, `remove()`, and `map()` return `None` and change the original object

* Uses **imperative programming** with loops and direct array manipulation

### Lab 2 (Immutable)

* **Creates new instances** for every operation

* Methods like `cons()`, `remove()`, and `map()` return new `DynamicArray` objects
 
* Uses **functional programming** with recursion and immutable data structures

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
