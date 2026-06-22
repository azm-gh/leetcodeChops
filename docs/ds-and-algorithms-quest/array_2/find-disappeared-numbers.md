# Q3. Find All Numbers Disappeared in an Array

**LeetCode:** [448](https://leetcode.com/problems/find-all-numbers-disappeared-in-an-array/)

## Intuition

Values are in [1, n] but some are missing. The naive approach uses a hash set of present values. The optimized approach marks visited indices in-place by negating the value at the corresponding index. After processing, indices with positive values are the missing numbers — O(1) extra space.

## Solutions

### `find_disappeared_numbers_naive` — Naive

```python
def find_disappeared_numbers_naive(nums: List[int]) -> List[int]:
    n = len(nums)
    present = set(nums)
    result = []
    for i in range(1, n + 1):
        if i not in present:
            result.append(i)
    return result
```

### `find_disappeared_numbers_optimized` — Optimized

```python
def find_disappeared_numbers_optimized(nums: List[int]) -> List[int]:
    n = len(nums)
    for num in nums:
        idx = abs(num) - 1
        if nums[idx] > 0:
            nums[idx] = -nums[idx]
    result = []
    for i in range(n):
        if nums[i] > 0:
            result.append(i + 1)
    return result
```
