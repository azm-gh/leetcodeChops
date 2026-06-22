# Q2. Shuffle the Array

**LeetCode:** [1470](https://leetcode.com/problems/shuffle-the-array/)

## Pattern

**Two-pointer approach** — We effectively use two pointers: one at index `i` tracking the x-half and one at `i + n` tracking the y-half. The pointers advance together, interleaving the elements. This maps directly to the two-pointer pattern under "pairing or interleaving two sequences."

## Intuition

The array has 2n elements where the first n are x's and the last n are y's. The result interleaves them: x1, y1, x2, y2, ..., xn, yn. Both solutions are O(n); the optimized version pre-allocates the result array.

## Solutions

### `shuffle_naive` — Naive

```python
def shuffle_naive(nums: List[int], n: int) -> List[int]:
    result = []
    for i in range(n):
        result.append(nums[i])
        result.append(nums[i + n])
    return result
```

### `shuffle_optimized` — Optimized

```python
def shuffle_optimized(nums: List[int], n: int) -> List[int]:
    result = [0] * (2 * n)
    for i in range(n):
        result[2 * i] = nums[i]
        result[2 * i + 1] = nums[i + n]
    return result
```
