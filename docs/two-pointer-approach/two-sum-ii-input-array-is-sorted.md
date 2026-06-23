# Two Sum II - Input Array Is Sorted

**LeetCode:** [https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/)

**AlgoMaster Animation:** [https://algomaster.io/animations/dsa/two-sum-ii-input-array-is-sorted](https://algomaster.io/animations/dsa/two-sum-ii-input-array-is-sorted)

## Intuition

Intuition: Two-pointer works because the array is sorted. Starting with one
pointer at each end, we can adjust the sum: if the sum is too small, move the
left pointer right (increase sum); if too large, move the right pointer left
(decrease sum). We converge toward the target in O(n) time.

## Solutions

### `two_sum_naive` — Naive

```python
def two_sum_naive(numbers: List[int], target: int) -> List[int]:
    # Time: O(n^2) — check every pair
    # Space: O(1)
    n = len(numbers)
    for i in range(n):
        for j in range(i + 1, n):
            if numbers[i] + numbers[j] == target:
                return [i + 1, j + 1]
    return []
```

### `two_sum_optimized` — Optimized

```python
def two_sum_optimized(numbers: List[int], target: int) -> List[int]:
    # Time: O(n) — two-pointer converges in one pass (array is sorted)
    # Space: O(1)
    left, right = 0, len(numbers) - 1
    while left < right:
        curr = numbers[left] + numbers[right]
        if curr == target:
            return [left + 1, right + 1]
        if curr < target:
            left += 1
        else:
            right -= 1
    return []
```
