from typing import NamedTuple, Deque
from collections import deque

import aoc

grid = aoc.getCellsForDay(23)
# grid = aoc.getCellsForDay(23, force_filepath="inputs/day23_example.txt")
# grid = aoc.getCellsForDay(23, force_filepath="inputs/day23_simple.txt")

sizeY = len(grid)
sizeX = len(grid[0])

print("sizeY", sizeY)
print("sizeX", sizeX)


class Point(NamedTuple):
    x: int
    y: int


S: Point = Point(-1, -1)
E: Point = Point(sizeX + 1, sizeY + 1)


for y, line in enumerate(grid):
    for x, cell in enumerate(line):
        if y == 0 and cell == ".":
            S = Point(x, y)
        if y == sizeY - 1 and cell == ".":
            E = Point(x, y)

print("S", S)
print("E", S)

slopeMap = {
    "^": Point(0, -1),
    "v": Point(0, 1),
    ">": Point(1, 0),
    "<": Point(-1, 0),
}


Path = tuple[Point, ...]


def getLongestPath(respectSlope) -> Path:
    currentPaths: Deque[Path] = deque([(S,)])
    validPaths: Deque[Path] = deque()

    while len(currentPaths) > 0:
        path: Path = currentPaths.pop()
        assert len(path) > 0

        lastP = path[-1]
        assert lastP

        if lastP == E:
            validPaths.append(path)
            continue

        # Determine next points
        nextPoints: set[Point] = set()
        cell = grid[lastP.y][lastP.x]
        if respectSlope and cell in slopeMap:
            direction = slopeMap[cell]
            nextPoint = Point(lastP.x + direction.x, lastP.y + direction.y)
            if nextPoint in path:
                # current path is invalid
                continue
            assert grid[nextPoint.y][nextPoint.x] != "#"
            nextPoints.add(nextPoint)
        else:
            neighbors = (
                Point(lastP.x + 1, lastP.y),
                Point(lastP.x - 1, lastP.y),
                Point(lastP.x, lastP.y + 1),
                Point(lastP.x, lastP.y - 1),
            )
            # Filter out unwanted next points
            for n in neighbors:
                if (
                    n not in path
                    and n.x >= 0
                    and n.y >= 0
                    and n.x < sizeX
                    and n.y < sizeY
                    and grid[n.y][n.x] != "#"
                ):
                    nextPoints.add(n)

        if len(nextPoints) == 0:
            # current path is invalid
            continue

        # Explore the different possible paths
        for nextPoint in nextPoints:
            newPath = (*path, nextPoint)
            currentPaths.append(newPath)

    assert len(validPaths) > 0
    # remove the S to have the correct count
    bestPath = max(validPaths, key=lambda p: len(p))
    assert bestPath[0] == S
    return bestPath[1:]


bestPath1 = getLongestPath(respectSlope=True)
print("Part 1", len(bestPath1))
print(aoc.getTick())

if sizeX < 20:
    for y, line in enumerate(grid):
        for x, cell in enumerate(line):
            if (x, y) in bestPath1:
                print("O", end="")
            else:
                print(cell, end="")
        print("", end="\n")

bestPaht2 = getLongestPath(respectSlope=False)
print("Part 2", len(bestPaht2))
print(aoc.getTick())
