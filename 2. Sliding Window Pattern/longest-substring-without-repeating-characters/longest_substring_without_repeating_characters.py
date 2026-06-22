"""
LeetCode 3: Longest Substring Without Repeating Characters
https://leetcode.com/problems/longest-substring-without-repeating-characters/
"""


# Intuition: Variable-size sliding window. Expand right pointer to add new
# characters. When a repeat is found, shrink left pointer past the previous
# occurrence. The window always contains unique characters, tracked by a dict
# mapping character to its last seen index. This gives O(n) instead of O(n^2).


def length_of_longest_substring_naive(s: str) -> int:
    n = len(s)
    max_len = 0
    for i in range(n):
        seen = set()
        for j in range(i, n):
            if s[j] in seen:
                break
            seen.add(s[j])
            max_len = max(max_len, j - i + 1)
    return max_len


def length_of_longest_substring_optimized(s: str) -> int:
    char_index = {}
    left = 0
    max_len = 0
    for right, ch in enumerate(s):
        if ch in char_index and char_index[ch] >= left:
            left = char_index[ch] + 1
        char_index[ch] = right
        max_len = max(max_len, right - left + 1)
    return max_len
