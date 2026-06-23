# Q2. How Many Numbers Are Smaller Than the Current Number

**LeetCode:** [1365](https://leetcode.com/problems/how-many-numbers-are-smaller-than-the-current-number/)

## Pattern

**Prefix sum (counting sort variant)** — Since values are bounded (0..100), we build a frequency array and compute prefix sums. The prefix sum at each value tells us how many elements are ≤ that value. Subtracting the current element's own count gives "smaller than." This is the prefix sum pattern applied to a fixed-range frequency domain.

## Intuition

For each number we need the count of smaller numbers in the array. The naive approach checks every pair in O(n²). Since values are bounded (0..100), the optimized approach uses counting sort: build a frequency array, compute prefix sums to know how many numbers are smaller than each value, then look up the result for each input in O(1).

## Solutions

### `smaller_numbers_than_current_naive` — Naive

```python
def smaller_numbers_than_current_naive(nums: List[int]) -> List[int]:
    n = len(nums)
    result = []
    for i in range(n):
        count = 0
        for j in range(n):
            if i != j and nums[j] < nums[i]:
                count += 1
        result.append(count)
    return result
```

### `smaller_numbers_than_current_optimized` — Optimized

```python
def smaller_numbers_than_current_optimized(nums: List[int]) -> List[int]:
    freq = [0] * 101
    for num in nums:
        freq[num] += 1
    prefix = 0
    smaller = [0] * 101
    for i in range(101):
        smaller[i] = prefix
        prefix += freq[i]
    return [smaller[num] for num in nums]
```
