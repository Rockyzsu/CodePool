#!/usr/bin/python3
"""
We define a harmonious array is an array where the difference between its
maximum value and its minimum value is exactly 1.

Now, given an integer array, you need to find the length of its longest
harmonious subsequence among all its possible subsequences.

Example 1:
Input: [1,3,2,2,5,2,3,7]
Output: 5

Explanation: The longest harmonious subsequence is [3,2,2,2,3].
Note: The length of the input array will not exceed 20,000.
"""
from typing import List
from collections import defaultdict


class Solution:
    def findLHS(self, nums: List[int]) -> int:
        """
        counter and iterate
        """
        counter = defaultdict(int)
        for n in nums:
            counter[n] += 1

        ret = 0
        for k, v in counter.items():
            if k + 1 in counter:
                ret = max(ret, v + counter[k + 1])

        return ret
