from enum import Enum
from typing import NamedTuple

import aoc

data = aoc.getLinesForDay(18)
data = aoc.getLinesForDay(18, force_filepath="inputs/day18_example.txt")


class Point(NamedTuple):
    x: int
    y: int


Segment = tuple[Point, Point]

Color = str


class DIRECTION(Enum):
    U = Point(0, -1)
    R = Point(1, 0)
    D = Point(0, 1)
    L = Point(-1, 0)


class PlanLine(NamedTuple):
    dir: DIRECTION
    length: int
    color: str


digPlan: list[PlanLine] = []
for line in data:
    [direction, length, color] = line.split()
    digPlan.append(PlanLine(DIRECTION[direction], int(length), color[1:-1]))


def getCorners(instructions: list[PlanLine]) -> list[Point]:
    corners: list[Point] = []
    corners.append(Point(0, 0))
    currentPoint = Point(0, 0)
    for line in instructions:
        newPoint = Point(
            currentPoint.x + line.dir.value.x * line.length,
            currentPoint.y + line.dir.value.y * line.length,
        )
        corners.append(newPoint)
        currentPoint = newPoint

    assert currentPoint == Point(0, 0)
    return corners


def getEdges(instructions: list[PlanLine]) -> set[Point]:
    edges: set[Point] = set()
    edges.add(Point(0, 0))
    currentPoint = Point(0, 0)
    for line in instructions:
        for _ in range(line.length):
            newPoint = Point(
                currentPoint.x + line.dir.value.x, currentPoint.y + line.dir.value.y
            )
            edges.add(newPoint)
            currentPoint = newPoint

    return edges


def getInside(edges: set[Point]) -> set[Point]:
    # Bucket-fill every point to check if they are inside
    outside: set[Point] = set()
    inside: set[Point] = set()

    minX = min([p.x for p in edges])
    maxX = max([p.x for p in edges])
    minY = min([p.y for p in edges])
    maxY = max([p.y for p in edges])

    print("area to consider", (maxY - minY) * (maxX - minX))

    def get4Neighs(p: Point):
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            yield Point(p.x + dx, p.y + dy)

    def isOutOfBounds(p: Point) -> bool:
        return p.x < minX or p.x > maxX or p.y < minY or p.y > maxY

    for x in range(minX, maxX + 1):
        for y in range(minY, maxY + 1):
            p = Point(x, y)
            if p in edges or p in outside or p in inside:
                continue

            seen: set[Point] = set([p])
            toReview: set[Point] = set([p])
            hasSeenOutside = False
            while len(toReview) > 0:
                fillP = toReview.pop()
                for n in get4Neighs(fillP):
                    if n in seen:
                        continue

                    if isOutOfBounds(n):
                        hasSeenOutside = True
                        continue

                    elif n not in edges:
                        seen.add(n)
                        toReview.add(n)

            if hasSeenOutside:
                outside.update(seen)
            else:
                inside.update(seen)
    return inside


def isHorizontalSegment(segment: Segment) -> bool:
    return segment[0].y == segment[1].y


def intersectsScanLine(segment: Segment, scanY: int):
    if isHorizontalSegment(segment):
        return scanY == segment[0].y
    else:
        assert segment[0].x == segment[1].x
        y1 = segment[0].y
        y2 = segment[1].y
        for segY in range(min(y1, y2), max(y1, y2) + 1):
            if segY == scanY:
                return True
        return False


def getInsideArea(corners: list[Point]) -> int:
    # Use a scanline algorithm to check line by line
    insideCount: int = 0

    lineSegments: set[Segment] = set()
    for pIdx in range(len(corners) - 1):
        lineSegments.add((corners[pIdx], corners[pIdx + 1]))
    lineSegments.add((corners[-1], corners[0]))

    minY: int = min([p.y for p in corners])
    maxY: int = max([p.y for p in corners])

    print("nb of lines", maxY - minY)
    for lineY in range(minY, maxY + 1):
        segmentsInLine: list[Segment] = sorted(
            [s for s in lineSegments if intersectsScanLine(s, lineY)],
            key=lambda seg: seg[0].x,
        )

        isIn = True
        inFrom = -1

        for s in segmentsInLine:
            if not isHorizontalSegment(s):
                isIn = not isIn
                if isIn:
                    inFrom = s[0].x
                else:
                    inLength = 1 + s[0].x - inFrom
                    insideCount += inLength
            else:
                if isIn:
                    pass  # Nothing to do, will be counted by the above
                else:
                    insideCount += abs(s[1].x - s[0].x)
                    

    return insideCount


edges = getEdges(digPlan)
corners = getCorners(digPlan)
print(len(corners), "corners and ", len(edges), "edges in", aoc.getTick())
inside = getInside(edges)
insideArea = getInsideArea(corners)

print("Part 1", len(edges) + len(inside))
print("vs.", insideArea)
print(aoc.getTick())

exit(0)

# Reverse instructions for Part 2


def reverseInstruction(instr: PlanLine) -> PlanLine:
    hexa = instr.color[1:]
    lengthHex = hexa[:5]
    dirHex = hexa[5]

    length = int(lengthHex, base=16)
    direction = [DIRECTION.R, DIRECTION.D, DIRECTION.L, DIRECTION.U][int(dirHex)]

    return PlanLine(direction, length, "no")


edges2 = getEdges([reverseInstruction(i) for i in digPlan])
print(len(edges2), "edges in", aoc.getTick())
inside2 = getInside(edges2)

print("Part 2", len(edges2) + len(inside2))
print(aoc.getTick())

# Solution might work (maybe?) but is too long
# Idea: use a clever line scan to count the ins and outs line by line?
