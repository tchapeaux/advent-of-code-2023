from typing import NamedTuple
from queue import PriorityQueue

import aoc

data = aoc.getCellsForDay(17)
data = aoc.getCellsForDay(17, force_filepath="inputs/day17_example.txt")
# data = aoc.getCellsForDay(17, force_filepath="inputs/day17_simple.txt")

data = [[int(c) for c in row] for row in data]

nbRows = len(data)
nbCols = len(data[0])


# This is dijkstra, right?


class Point(NamedTuple):
    x: int
    y: int


class PrevPoint(NamedTuple):
    point: Point
    dirX: int
    dirY: int
    straightCnt: int


start = Point(0, 0)


def isInBounds(point: Point) -> bool:
    return point.x >= 0 and point.x < nbCols and point.y >= 0 and point.y < nbRows


FOUR_NEIGHS = ((1, 0), (0, 1), (-1, 0), (0, -1))


def getNeighbors(point: Point, coords=FOUR_NEIGHS):
    for coord in coords:
        n = Point(point.x + coord[0], point.y + coord[1])
        if isInBounds(n):
            yield n


toVisit: PriorityQueue[tuple[int, Point]] = PriorityQueue()

bestDist: dict[Point, int] = {start: 0}
prevPoint: dict[Point, Point] = {}

for n in getNeighbors(start):
    toVisit.put((data[n.y][n.x], n))
    bestDist[n] = data[n.y][n.x]
    prevPoint[n] = start

while not toVisit.empty():
    (dist, point) = toVisit.get()

    neighCoords = FOUR_NEIGHS
    # Check if path is at least 3 points
    if (
        point in prevPoint
        and prevPoint[point] in prevPoint
        and prevPoint[prevPoint[point]] in prevPoint
    ):
        # Check if the 3 last points are aligned
        p1 = prevPoint[point]
        p2 = prevPoint[prevPoint[point]]
        p3 = prevPoint[prevPoint[prevPoint[point]]]

        dx1 = p1.x - point.x
        dx2 = p2.x - p1.x
        dx3 = p3.x - p2.x

        if abs(dx1 + dx2 + dx3) == 3:
            neighCoords = ((0, 1), (0, -1))

        dy1 = p1.y - point.y
        dy2 = p2.y - p1.y
        dy3 = p3.y - p2.y

        if abs(dy1 + dy2 + dy3) == 3:
            neighCoords = ((1, 0), (-1, 0))

    for n in getNeighbors(point, coords=neighCoords):
        nDist = dist + data[n.y][n.x]
        if n not in bestDist or bestDist[n] > nDist:
            bestDist[n] = nDist
            prevPoint[n] = point
            toVisit.put((nDist, n))

end = Point(nbCols - 1, nbRows - 1)
assert end in bestDist

# Reconstruct path
cur = end
path = [end]
while cur != start:
    print(cur)
    cur = prevPoint[cur]
    path.append(cur)

with open("day17_path.txt", "w") as f:
    s = ""
    for y in range(nbRows):
        for x in range(nbCols):
            s += "#" if Point(x, y) in path else "."
        s += "\n"
    f.write(s)

print(list(reversed(path)))

print("Part 1", bestDist[end])

# This doesn't work because there are multiple paths to the same point
# And the Dijkstra only keeps the first it discovers
# But the path allowing the best path might be a different one


# suggestion of strategy to explore:
# add the "last straight line" in the "best" calculation,
# allowing a "less straight-y" path to override a "more striaght-y" one
