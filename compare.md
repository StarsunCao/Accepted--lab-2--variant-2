# Mutable vs Immutable Dynamic Array Implementation

## Core Implementation Approaches

### Lab 1 (Mutable)

* **Modifies existing data** in-place
* Methods like `add()`, `remove()`,
and `map()` return `None` and
change the original object
* Uses **imperative programming** with loops and direct array manipulation

### Lab 2 (Immutable)

* **Creates new instances** for every operation
* Methods like `cons()`, `remove()`, and `map()` return new `DynamicArray` objects
* Uses **functional programming** with recursion and immutable data structures

## Pros and Cons Comparison

| Aspect | Mutable (Lab 1) | Immutable (Lab 2) |
|--------|----------------|-------------------|
| **Memory Efficiency** | ✅ Better for reusing memory | ❌ Higher memory usage |
| **Performance** | ✅ Faster for modifications | ❌ Overhead from copying data |
| **Thread Safety** | ❌ Prone to race conditions | ✅ Inherently thread-safe |
| **Debugging** | ❌ Hard to track state changes | ✅ Objects maintain state |
| **Reasoning** | ❌ Side effects are hard to track | ✅ Pure predictable functions |
| **Implementation** | ✅ Simpler operations | ❌ More complex for efficiency |
| **State History** | ❌ Lost after changes | ✅ Preserved (undo/redo) |
| **References** | ❌ Shared objects affect all refs | ✅ No unexpected changes |
| **Recursion** | ✅ Not limited by stack depth | ❌ May hit stack limits |