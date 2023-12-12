# Playground file
# This is just for small experiments during the jam
# Mostly useful for me when I forget what the exact Python syntax for something is

import aoc
import re

a = "aaaa>?<bbbb"
i = a.index("?")
print(a[:i])
print(a[i + 1 :])


def fooYield(recursive=True):
    yield 1
    yield 2
    yield 3
    if recursive:
        for foo in fooYield(recursive=False):
            yield foo


for foo in fooYield():
    print(foo)

a = (1, 2, 3)
print(tuple([*a * 5]))
