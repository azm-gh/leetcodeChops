"""
LeetCode 1365: How Many Numbers Are Smaller Than the Current Number
https://leetcode.com/problems/how-many-numbers-are-smaller-than-the-current-number/
"""
# Intuition: For each number, we need the count of numbers smaller than it.
# The naive approach checks every pair O(n^2). The optimized approach uses
# counting sort since values are bounded (0..100), computing a frequency
# array and prefix sums so each result is available in O(1).

from typing import List


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
