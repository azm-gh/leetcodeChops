# Q1. Set Mismatch

**LeetCode:** [645](https://leetcode.com/problems/set-mismatch/)

**AlgoMaster Animation:** [https://algomaster.io/animations/dsa/set-mismatch](https://algomaster.io/animations/dsa/set-mismatch)

## Pattern

**Hashmaps / Hash sets** — The naive solution uses a frequency array (essentially a hashmap with integer keys) to count occurrences. The optimized solution uses the math of set sums, still relying on set reasoning. This maps to "counting frequencies" and "have I seen this before?" from the hashmap pattern.

## Intuition

The array contains numbers from 1 to n, but one is duplicated and one is missing. The naive approach counts frequencies. The optimized approach uses the math property: the difference between actual sum and set sum gives the duplicate; the difference between expected sum (1..n) and set sum gives the missing number.

## Solutions

### `find_error_nums_naive` — Naive

```python
def find_error_nums_naive(nums: List[int]) -> List[int]:
    n = len(nums)
    freq = [0] * (n + 1)
    for num in nums:
        freq[num] += 1
    duplicate = missing = -1
    for i in range(1, n + 1):
        if freq[i] == 2:
            duplicate = i
        elif freq[i] == 0:
            missing = i
    return [duplicate, missing]
```

### `find_error_nums_optimized` — Optimized

```python
def find_error_nums_optimized(nums: List[int]) -> List[int]:
    n = len(nums)
    set_sum = sum(set(nums))
    actual_sum = sum(nums)
    expected_sum = n * (n + 1) // 2
    duplicate = actual_sum - set_sum
    missing = expected_sum - set_sum
    return [duplicate, missing]
```
