from typing import NamedTuple

import aoc

data = aoc.getCellsForDay(16)
# data = aoc.getCellsForDay(16, force_filepath="inputs/day16_example.txt")
# data = aoc.getCellsForDay(16, force_filepath="inputs/day16_simple.txt")


class BeamEnd(NamedTuple):
    x: int
    y: int
    dirX: int
    dirY: int


class Point(NamedTuple):
    x: int
    y: int


nbRows = len(data)
nbCols = len(data[0])


# print("nbRows", nbRows, "nbCols", nbCols)


def isOutOfBound(p: Point) -> bool:
    return p.x < 0 or p.x >= nbCols or p.y < 0 or p.y >= nbRows


def getEnergizedGridFrom(startBeam: BeamEnd):
    beams: list[BeamEnd] = [startBeam]

    energized: dict[Point, set[BeamEnd]] = dict()
    energized[Point(startBeam.x, startBeam.y)] = set([startBeam])

    step = 0
    while len(beams) > 0:
        newBeams: list[BeamEnd] = []
        # print(step, len(beams))

        for beam in beams:
            # print("\t", beam, end="\t")

            if isOutOfBound(Point(beam.x, beam.y)):
                # print("skip")
                continue

            # print(data[beam.y][beam.x])

            if data[beam.y][beam.x] == "\\":
                if beam.dirX == 1:
                    newBeams.append(BeamEnd(beam.x, beam.y + 1, 0, 1))
                elif beam.dirX == -1:
                    newBeams.append(BeamEnd(beam.x, beam.y - 1, 0, -1))
                elif beam.dirY == 1:
                    newBeams.append(BeamEnd(beam.x + 1, beam.y, 1, 0))
                elif beam.dirY == -1:
                    newBeams.append(BeamEnd(beam.x - 1, beam.y, -1, 0))

            elif data[beam.y][beam.x] == "/":
                if beam.dirX == 1:
                    newBeams.append(BeamEnd(beam.x, beam.y - 1, 0, -1))
                elif beam.dirX == -1:
                    newBeams.append(BeamEnd(beam.x, beam.y + 1, 0, 1))
                elif beam.dirY == 1:
                    newBeams.append(BeamEnd(beam.x - 1, beam.y, -1, 0))
                elif beam.dirY == -1:
                    newBeams.append(BeamEnd(beam.x + 1, beam.y, 1, 0))

            elif data[beam.y][beam.x] == "|":
                if abs(beam.dirX) == 1:
                    newBeams.append(BeamEnd(beam.x, beam.y - 1, 0, -1))
                    newBeams.append(BeamEnd(beam.x, beam.y + 1, 0, 1))
                else:
                    newBeams.append(
                        BeamEnd(
                            beam.x + beam.dirX, beam.y + beam.dirY, beam.dirX, beam.dirY
                        )
                    )

            elif data[beam.y][beam.x] == "-":
                if abs(beam.dirY) == 1:
                    newBeams.append(BeamEnd(beam.x + 1, beam.y, 1, 0))
                    newBeams.append(BeamEnd(beam.x - 1, beam.y, -1, 0))
                else:
                    newBeams.append(
                        BeamEnd(
                            beam.x + beam.dirX, beam.y + beam.dirY, beam.dirX, beam.dirY
                        )
                    )

            else:
                assert data[beam.y][beam.x] == "."
                newBeams.append(
                    BeamEnd(
                        beam.x + beam.dirX, beam.y + beam.dirY, beam.dirX, beam.dirY
                    )
                )

        beamsToRemove = set()
        for b in newBeams:
            point = Point(b.x, b.y)

            if isOutOfBound(point):
                beamsToRemove.add(b)
                continue

            if point not in energized:
                energized[point] = set()

            if b in energized[point]:
                beamsToRemove.add(b)
            else:
                energized[Point(b.x, b.y)].add(b)
        newBeams = [b for b in newBeams if b not in beamsToRemove]

        beams = newBeams
        step += 1

    return energized


energizedPart1 = getEnergizedGridFrom(BeamEnd(0, 0, 1, 0))

with open("day16_energized.txt", "w") as f:
    s = ""
    for y in range(nbRows):
        for x in range(nbCols):
            if Point(x, y) in energizedPart1:
                s += "#"
            else:
                s += "."
        s += "\n"
    f.write(s)

print("Part 1", len(energizedPart1))
print(aoc.getTick())

# x too high (was counting some cells outside the grid)

possibleStarts = [
    # UPPER EDGE
    *[BeamEnd(x, 0, 0, 1) for x in range(nbCols)],
    # LEFT EDGE
    *[BeamEnd(0, y, 1, 0) for y in range(nbRows)],
    # BOTTOM EDGE
    *[BeamEnd(x, nbRows - 1, 0, -1) for x in range(nbCols)],
    # RIGHT EDGE
    *[BeamEnd(nbCols - 1, y, -1, 0) for y in range(nbRows)],
]

bestStart = None
energizedBest = set()
energizedBestCount = -1
for start in possibleStarts:
    print("Start from", start)
    energized = getEnergizedGridFrom(start)
    print("=>", len(energized))
    if len(energized) > energizedBestCount:
        print("Current best")
        energizedBestCount = len(energized)
        energizedBest = energized
        bestStart = start

print("Best", bestStart)

with open("day16_energized_best.txt", "w") as f:
    s = ""
    for y in range(nbRows):
        for x in range(nbCols):
            if Point(x, y) in energizedBest:
                s += "#"
            else:
                s += "."
        s += "\n"
    f.write(s)

print("Part 2", energizedBestCount)
print(aoc.getTick())

# 8023 too low
# 8024 too low

# Unfortunately, no time to debug :(
