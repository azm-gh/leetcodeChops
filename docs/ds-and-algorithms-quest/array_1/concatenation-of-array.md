# Q1. Concatenation of Array

**LeetCode:** [1929](https://leetcode.com/problems/concatenation-of-array/)

## Intuition

The result is simply the input array repeated twice. The naive approach copies elements one by one into a new array; the optimized approach uses Python's list concatenation.

## Solutions

### `get_concatenation_naive` — Naive

```python
def get_concatenation_naive(nums: List[int]) -> List[int]:
    n = len(nums)
    ans = [0] * (2 * n)
    for i in range(n):
        ans[i] = nums[i]
        ans[i + n] = nums[i]
    return ans
```

### `get_concatenation_optimized` — Optimized

```python
def get_concatenation_optimized(nums: List[int]) -> List[int]:
    return nums + nums
```
