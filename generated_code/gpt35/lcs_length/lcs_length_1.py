def lcs_length(s, t):
    dp = {}

    for i in range(len(s)):
        for j in range(len(t)):
            if s[i] == t[j]:
                dp[i, j] = dp.get((i - 1, j), 0) + 1

    return max(dp.values()) if dp else 0