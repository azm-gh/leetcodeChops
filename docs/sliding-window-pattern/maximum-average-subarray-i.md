# Maximum Average Subarray I

**LeetCode:** [https://leetcode.com/problems/maximum-average-subarray-i/](https://leetcode.com/problems/maximum-average-subarray-i/)

## Intuition

Intuition: Fixed-size sliding window. Since k is constant, we slide a window
of size k across the array, subtracting the outgoing element and adding the
incoming one. This maintains the window sum in O(1) per step instead of
recalculating from scratch O(n*k).

## Solutions

### `find_max_average_naive` — Naive

```python
def find_max_average_naive(nums: List[int], k: int) -> float:
    n = len(nums)
    max_avg = float("-inf")
    for i in range(n - k + 1):
        total = 0
        for j in range(i, i + k):
            total += nums[j]
        max_avg = max(max_avg, total / k)
    return max_avg
```

### `find_max_average_optimized` — Optimized

```python
def find_max_average_optimized(nums: List[int], k: int) -> float:
    n = len(nums)
    window_sum = sum(nums[:k])
    max_sum = window_sum
    for i in range(k, n):
        window_sum += nums[i] - nums[i - k]
        max_sum = max(max_sum, window_sum)
    return max_sum / k
```
