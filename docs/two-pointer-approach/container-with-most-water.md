# Container With Most Water

**LeetCode:** [https://leetcode.com/problems/container-with-most-water/](https://leetcode.com/problems/container-with-most-water/)

**AlgoMaster Animation:** [https://algomaster.io/animations/dsa/container-with-most-water](https://algomaster.io/animations/dsa/container-with-most-water)

## Intuition

Intuition: Two-pointer from both ends works because area is limited by the
shorter line. Moving the shorter pointer inward may find a taller line, which
could increase area despite narrower width. We never move the taller pointer
because that would only decrease width without potential height gain.

## Solutions

### `max_area_naive` — Naive

```python
def max_area_naive(height: List[int]) -> int:
    # Time: O(n^2) — check every pair of lines
    # Space: O(1)
    n = len(height)
    max_water = 0
    for i in range(n):
        for j in range(i + 1, n):
            area = min(height[i], height[j]) * (j - i)
            max_water = max(max_water, area)
    return max_water
```

### `max_area_optimized` — Optimized

```python
def max_area_optimized(height: List[int]) -> int:
    # Time: O(n) — single pass from both ends
    # Space: O(1)
    left, right = 0, len(height) - 1
    max_water = 0
    while left < right:
        h = min(height[left], height[right])
        w = right - left
        max_water = max(max_water, h * w)
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    return max_water
```
