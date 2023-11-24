def sieve(max):
    if max < 2:
        return []
    
    primes = [2]
    for n in range(3, max + 1, 2):
        if all(n % p != 0 for p in primes):
            primes.append(n)
    return primes