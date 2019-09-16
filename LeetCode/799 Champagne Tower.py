#!/usr/bin/python3
"""
We stack glasses in a pyramid, where the first row has 1 glass, the second row
has 2 glasses, and so on until the 100th row.  Each glass holds one cup (250ml)
of champagne.

Then, some champagne is poured in the first glass at the top.  When the top most
glass is full, any excess liquid poured will fall equally to the glass
immediately to the left and right of it.  When those glasses become full, any
excess champagne will fall equally to the left and right of those glasses, and
so on.  (A glass at the bottom row has it's excess champagne fall on the floor.)

For example, after one cup of champagne is poured, the top most glass is full.
After two cups of champagne are poured, the two glasses on the second row are
half full.  After three cups of champagne are poured, those two cups become full
- there are 3 full glasses total now.  After four cups of champagne are poured,
the third row has the middle glass half full, and the two outside glasses are a
quarter full, as pictured below.



Now after pouring some non-negative integer cups of champagne, return how full
the j-th glass in the i-th row is (both i and j are 0 indexed.)



Example 1:
Input: poured = 1, query_glass = 1, query_row = 1
Output: 0.0
Explanation: We poured 1 cup of champange to the top glass of the tower
(which is indexed as (0, 0)). There will be no excess liquid so all the glasses
under the top glass will remain empty.

Example 2:
Input: poured = 2, query_glass = 1, query_row = 1
Output: 0.5
Explanation: We poured 2 cups of champange to the top glass of the tower
(which is indexed as (0, 0)). There is one cup of excess liquid. The glass
indexed as (1, 0) and the glass indexed as (1, 1) will share the excess liquid
equally, and each will get half cup of champange.


Note:

poured will be in the range of [0, 10 ^ 9].
query_glass and query_row will be in the range of [0, 99].
"""
from collections import defaultdict


class Solution:
    def champagneTower(self, poured: int, query_row: int, query_glass: int) -> float:
        """
        Simulation
        Instead of keeping track of how much champagne should end up in a
        glass, keep track of the total amount of champagne that flows through a
        glass.
        """
        G = defaultdict(lambda: defaultdict(int))
        G[0][0] = poured
        for i in range(query_row):
            for j in range(i+1):  # i + 1 glasses at row i
                excess = max(0, G[i][j] - 1)
                G[i+1][j] += excess / 2
                G[i+1][j+1] += excess / 2

        return min(1, G[query_row][query_glass])
