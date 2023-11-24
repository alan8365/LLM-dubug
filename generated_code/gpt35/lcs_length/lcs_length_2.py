def lcs_length(s, t):
    from collections import Counter

    dp = Counter()

    for i in range(len(s)):
        for j in range(len(t)):
            if s[i] == t[j]:
                dp[i, j] = dp[i - 1, j - 1] + 1

    return max(dp.values()) if dp else 0

The modification made was to change `dp[i, j] = dp[i - 1, j] + 1` to `dp[i, j] = dp[i - 1, j - 1] + 1`. This change ensures that the correct values are being added to the counter `dp`.