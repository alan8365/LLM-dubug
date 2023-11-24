def knapsack(capacity, items):
    memo = [[0] * (capacity + 1) for _ in range(len(items) + 1)]

    for i in range(1, len(items) + 1):
        weight, value = items[i - 1]

        for j in range(1, capacity + 1):
            memo[i][j] = memo[i - 1][j]

            if weight <= j:
                memo[i][j] = max(
                    memo[i][j],
                    value + memo[i - 1][j - weight]
                )

    return memo[len(items)][capacity]