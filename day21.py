from typing import NamedTuple

import aoc

data = aoc.getCellsForDay(21)


class Point(NamedTuple):
    x: int
    y: int


S: Point = Point(-1, -1)
rocks: set[Point] = set()


for y, line in enumerate(data):
    for x, cell in enumerate(line):
        if cell == "#":
            rocks.add(Point(x, y))
        if cell == "S":
            S = Point(x, y)

# Find closest distance of all tiles
# Then, count each tile of closest distance 64 or 64 - 2*i

distToS: dict[Point, int] = {}
distToS[S] = 0

for d in range(1, 64 + 1):
    prevDest = d - 1
    points = [p for p in distToS.keys() if distToS[p] == prevDest]

    for p in points:
        neighbors = [
            Point(p.x + 1, p.y),
            Point(p.x - 1, p.y),
            Point(p.x, p.y + 1),
            Point(p.x, p.y - 1),
        ]
        for n in neighbors:
            if n in rocks:
                continue
            if n in distToS:
                continue

            distToS[n] = d

part1Count = 0
for d in range(0, 64 + 1, 2):
    dCount = len([p for p in distToS.keys() if distToS[p] == d])
    print(d, dCount)
    part1Count += dCount

print("Part 1", part1Count)
