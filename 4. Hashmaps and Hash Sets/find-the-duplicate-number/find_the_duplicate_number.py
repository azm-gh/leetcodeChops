"""
LeetCode 287: Find the Duplicate Number
https://leetcode.com/problems/find-the-duplicate-number/
"""

# Intuition: The array values (1..n) act as linked list pointers into the
# array indices by value. Since there's a duplicate, it creates a cycle.
# Floyd's cycle detection (tortoise and hare) finds the cycle entrance,
# which is the duplicate value. O(n) time, O(1) space — no extra hashmap needed.

from typing import List


def find_duplicate_naive(nums: List[int]) -> int:
    seen = set()
    for num in nums:
        if num in seen:
            return num
        seen.add(num)
    return -1


def find_duplicate_optimized(nums: List[int]) -> int:
    slow = nums[0]
    fast = nums[0]
    while True:
        slow = nums[slow]
        fast = nums[nums[fast]]
        if slow == fast:
            break
    slow = nums[0]
    while slow != fast:
        slow = nums[slow]
        fast = nums[fast]
    return slow
