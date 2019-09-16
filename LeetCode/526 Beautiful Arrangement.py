#!/usr/bin/python3
"""
Suppose you have N integers from 1 to N. We define a beautiful arrangement as an
array that is constructed by these N numbers successfully if one of the
following is true for the ith position (1 <= i <= N) in this array:

The number at the ith position is divisible by i.
i is divisible by the number at the ith position.


Now given N, how many beautiful arrangements can you construct?

Example 1:

Input: 2
Output: 2
Explanation:

The first beautiful arrangement is [1, 2]:

Number at the 1st position (i=1) is 1, and 1 is divisible by i (i=1).

Number at the 2nd position (i=2) is 2, and 2 is divisible by i (i=2).

The second beautiful arrangement is [2, 1]:

Number at the 1st position (i=1) is 2, and 2 is divisible by i (i=1).

Number at the 2nd position (i=2) is 1, and i (i=2) is divisible by 1.


Note:

N is a positive integer and will not exceed 15.
"""


class Solution:
    def countArrangement(self, N: int) -> int:
        """
        dfs
        """
        candidates = set(range(1, N+1))
        ret = self.dfs(candidates, 1, N)
        return ret

    def dfs(self, candidates, i, N):
        if i > N:
            return 1

        ret = 0
        for c in candidates:
            if c % i == 0 or i % c == 0:
                candidates.remove(c)
                ret += self.dfs(candidates, i+1, N)
                candidates.add(c)
        return ret


if __name__ == "__main__":
    assert Solution().countArrangement(2) == 2
