from functools import lru_cache

@lru_cache(maxsize=None)
def slow_square(n):
    print(f"Calculating {n}²...")
    return n * n

print(slow_square(5))  # calculates
print(slow_square(5))  # instant, cached
