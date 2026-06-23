# Q3. Max Consecutive Ones

**LeetCode:** [485](https://leetcode.com/problems/max-consecutive-ones/)

**AlgoMaster Animation:** [https://algomaster.io/animations/dsa/max-consecutive-ones](https://algomaster.io/animations/dsa/max-consecutive-ones)

## Pattern

**Sliding window (variable-size)** — The window represents the current run of consecutive 1s. When we hit a 0, the window resets (closes). When we see a 1, the window expands. We track the maximum window length seen. This is a simpler form of the sliding window where the condition for resetting is hitting a 0.

## Intuition

Scan linearly: when we see a 1, increment a running count and update the max; when we see a 0, reset the count. The naive approach uses nested loops to find each run; the optimized single-pass approach is both simpler and faster.

## Solutions

### `find_max_consecutive_ones_naive` — Naive

```python
def find_max_consecutive_ones_naive(nums: List[int]) -> int:
    n = len(nums)
    max_len = 0
    i = 0
    while i < n:
        if nums[i] == 1:
            j = i
            while j < n and nums[j] == 1:
                j += 1
            max_len = max(max_len, j - i)
            i = j
        else:
            i += 1
    return max_len
```

### `find_max_consecutive_ones_optimized` — Optimized

```python
def find_max_consecutive_ones_optimized(nums: List[int]) -> int:
    count = 0
    max_count = 0
    for num in nums:
        if num == 1:
            count += 1
            max_count = max(max_count, count)
        else:
            count = 0
    return max_count
```
