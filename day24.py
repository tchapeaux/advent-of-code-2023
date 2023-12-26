from typing import NamedTuple
import re

import aoc

lines = aoc.getLinesForDay(24)


class Hailstone(NamedTuple):
    x: int
    y: int
    z: int
    vx: int
    vy: int
    vz: int


class Point(NamedTuple):
    x: int
    y: int


hailstones: set[Hailstone] = set()
for line in lines:
    x, y, z, vx, vy, vz = re.findall(r"-?\d+", line)
    hailstones.add(Hailstone(x, y, z, vx, vy, vz))


def intersectAt2d(hail1, hail2) -> Point:
    pass


print(hailstones)
