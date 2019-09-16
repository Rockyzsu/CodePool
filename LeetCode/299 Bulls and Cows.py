from collections import defaultdict

__author__ = 'Daniel'


class Solution(object):
    def getHint(self, secret, guess):
        """
        :type secret: str
        :type guess: str
        :rtype: str
        """
        cnt = defaultdict(int)
        A = 0
        B = 0
        for c in secret:
            cnt[c] += 1

        for i, v in enumerate(guess):
            if v == secret[i]:
                A += 1
                cnt[v] -= 1
                if cnt[v] < 0:
                    # revert matched B
                    assert cnt[v] == -1
                    B -= 1
                    cnt[v] = 0

            elif cnt[v] > 0:
                B += 1
                cnt[v] -= 1

        return "%dA%dB" % (A, B)


if __name__ == "__main__":
    assert Solution().getHint("0", "1") == "0A0B"
