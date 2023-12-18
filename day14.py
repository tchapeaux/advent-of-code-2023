import json

import aoc

data = aoc.getCellsForDay(14)
# data = aoc.getCellsForDay(14, force_filepath="inputs/day14_example.txt")
data = aoc.getCellsForDay(14, force_filepath="inputs/day14_simple.txt")

Coord = tuple[int, int]

nbRows = len(data)
nbCols = len(data[0])

rounded: set[Coord] = set()
cubic: set[Coord] = set()
for y, line in enumerate(data):
    for x, cell in enumerate(line):
        if cell == "O":
            rounded.add((x, y))
        if cell == "#":
            cubic.add((x, y))


def findNewRounded(rounded: set[Coord], cubic: set[Coord], isX: bool, isAsc: bool):
    newRounded: set[Coord] = set()

    coordIdx = 0 if isX else 1
    step = 1 if isAsc else -1
    maxCoord = nbCols if isX else nbRows

    # Explore line by line depending on the direction
    lineCnt = maxCoord
    for lineIdx in range(lineCnt):
        lineIdx = (lineCnt - 1 - lineIdx) if isAsc else lineIdx
        roundedInLine: list[Coord] = sorted(
            [r for r in rounded if r[coordIdx] == lineIdx],
            key=lambda r: r[1 - coordIdx],
        )

        for round in roundedInLine:
            # Find new position by going line by line in the direction
            newLineIdx = round[coordIdx]
            while True:
                pos: Coord = (newLineIdx, round[1]) if isX else (round[0], newLineIdx)
                nextPos: Coord = (
                    (newLineIdx + step, round[1])
                    if isX
                    else (round[0], newLineIdx + step)
                )

                if nextPos[coordIdx] < 0 or nextPos[coordIdx] >= maxCoord:
                    newRounded.add(pos)
                    break

                if nextPos in newRounded or nextPos in cubic:
                    # stop here
                    newRounded.add(pos)
                    break

                newLineIdx += step

    return newRounded


roundedAfterPart1 = findNewRounded(rounded, cubic, isX=False, isAsc=False)


def getTotalLoad(rounded):
    return sum([nbRows - r[1] for r in rounded])


def printGrid(rounded, cubic):
    for y in range(nbRows):
        for x in range(len(data[0])):
            pos = (x, y)
            if pos in cubic:
                print("#", end="")
            elif pos in rounded:
                print("O", end="")
            else:
                print(".", end="")
        print("")


printGrid(roundedAfterPart1, cubic)

print(
    "Part 1",
    getTotalLoad(roundedAfterPart1),
)


def doCycle(rounded, cubic):
    newRounded = rounded
    # NORTH
    newRounded = findNewRounded(newRounded, cubic, isX=False, isAsc=False)
    # WEST
    newRounded = findNewRounded(newRounded, cubic, isX=True, isAsc=False)
    # SOUTH
    newRounded = findNewRounded(newRounded, cubic, isX=False, isAsc=True)
    # EAST
    newRounded = findNewRounded(newRounded, cubic, isX=True, isAsc=True)

    return newRounded


# We assume that there will be a loop when applying cycles
# So we look for repetition

roundedPart2 = rounded
roundedSeen: dict[str, int] = dict()
cycleCnt = 0

loopLength = None
loopStart = None

print("Looking for cycle...")
while True:
    roundedPart2 = doCycle(roundedPart2, cubic)
    cycleCnt += 1

    canonicalRounded = json.dumps(sorted(roundedPart2))

    if canonicalRounded not in roundedSeen:
        roundedSeen[canonicalRounded] = cycleCnt
    else:
        print("FOUND CYCLE", cycleCnt, roundedSeen[canonicalRounded])
        loopStart = roundedSeen[canonicalRounded]
        loopLength = cycleCnt - loopStart
        break

TARGET = 1000000000

cycleSameAsTarget = loopStart + ((TARGET - loopStart) % loopLength)
print(cycleSameAsTarget)

finalRoundedPart2Json = [
    r for r in roundedSeen.keys() if roundedSeen[r] == cycleSameAsTarget
][0]

finalRoundedPart2 = json.loads(finalRoundedPart2Json)

printGrid(finalRoundedPart2, cubic)

print("Part 2", getTotalLoad(finalRoundedPart2))
