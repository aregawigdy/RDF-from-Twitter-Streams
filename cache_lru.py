
import time
import timeit
import functools


@functools.lru_cache(maxsize=128)
def fibonacci(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)


start_time = time.time()
print(fibonacci(35))
print("--- %s seconds ---" % (time.time() - start_time))
start_time = time.time()
print(fibonacci(35))
print("--- %s seconds ---" % (time.time() - start_time))
start_time = time.time()
print(fibonacci(35))
print("--- %s seconds ---" % (time.time() - start_time))
"""print(timeit.timeit('fibonacci(35)', globals=globals(), number=1))
print(timeit.timeit('fibonacci(35)', globals=globals(), number=1))
print(timeit.timeit('fibonacci(35)', globals=globals(), number=1))"""
