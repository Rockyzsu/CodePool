"""
There are n bulbs that are initially off. You first turn on all the bulbs. Then, you turn off every second bulb. On the
third round, you toggle every third bulb (turning on if it's off or turning off if it's on). For the nth round, you only
toggle the last bulb. Find how many bulbs are on after n rounds.

Example:

Given n = 3.

At first, the three bulbs are [off, off, off].
After first round, the three bulbs are [on, on, on].
After second round, the three bulbs are [on, off, on].
After third round, the three bulbs are [on, off, off].

So you should return 1, because there is only one bulb is on.
"""
import math

__author__ = 'Daniel'


class Solution(object):
    def bulbSwitch(self, n):
        """
        Only bulbs with index being a perfect square number toggled odd number of times
        Brainteaser
        :type n: int
        :rtype: int
        """
        cnt = int(math.sqrt(n))
        return cnt


