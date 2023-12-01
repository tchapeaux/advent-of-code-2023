# Playground file
# This is just for small experiments during the jam
# Mostly useful for me when I forget what the exact Python syntax for something is

import aoc
import re

print("hello there")

aoc.getInputForDay(1)


print(re.search(r"x*", "xxxx"))

listOfList = [[0, 0] for _ in range(4)]
listOfList[0][1] = 1
print(listOfList)

findNumbersRegex = r"(-?\d+)"
print(
    re.findall(
        findNumbersRegex, "Sensor at x=12, y=14: closest beacon is at x=-10, y=16"
    )
)

a = (53, "ABC")
b = (2, "DEF")
c = (2, "A")

print(tuple(sorted([a, b, c])))


a = "0123456789"

print(a[:-3])
print(a[-3:])

from enum import Enum


class MyEnum(Enum):
    FOO = 1
    BAR = 2
    ZAB = 3


for e in MyEnum:
    print(e)

a = {"a": 3, "b": 2}
b = {"a": 3, "b": 2}
print(a is b)
print(frozenset(a) is frozenset(b))
print(a == b)
