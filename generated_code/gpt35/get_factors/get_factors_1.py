def get_factors(n):
    if n == 1:
        return []

    factors = []
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            factors.append(i)
            if n // i != i:
                factors.append(n // i)

    return factors