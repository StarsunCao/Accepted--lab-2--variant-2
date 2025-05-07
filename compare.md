```markdown
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
|--------|----------------|-------------------|
| **Memory Efficiency** | ✅ Better for frequent modifications as it reuses memory | ❌ Higher memory usage due to creating new objects |
| **Performance** | ✅ Typically faster for modifications | ❌ Overhead from copying data structures |
| **Thread Safety** | ❌ Prone to race conditions | ✅ Inherently thread-safe |
| **Debugging** | ❌ Harder to track state changes | ✅ Easier as objects maintain their state |
| **Reasoning** | ❌ Side effects can be difficult to track | ✅ Pure functions with predictable outputs |
| **Implementation** | ✅ Simpler for many operations | ❌ More complex to maintain efficiency |
| **State History** | ❌ Lost after modifications | ✅ Preserved (enables undo/redo) |
| **Reference Problems** | ❌ Changes to shared objects affect all references | ✅ No unexpected changes through references |
| **Recursion Limits** | ✅ Not constrained by stack depth | ❌ May hit stack limits with recursive implementations |
```
