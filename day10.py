from typing import Optional

import aoc


data = aoc.getCellsForDay(10)
# data = aoc.getCellsForDay(10, force_filepath="inputs/day10_example_part2_simple.txt")


def getTileAt(x, y):
    return data[y][x]


Coord = tuple[int, int]
RelativeCoord = Coord

NORTH: RelativeCoord = (0, -1)
SOUTH: RelativeCoord = (0, 1)
WEST: RelativeCoord = (-1, 0)
EAST: RelativeCoord = (1, 0)


TILEMAP: dict[str, set[RelativeCoord]] = {
    # Format: set of linked coordinates
    "|": set([NORTH, SOUTH]),
    "-": set([EAST, WEST]),
    "L": set([NORTH, EAST]),
    "J": set([WEST, NORTH]),
    "7": set([SOUTH, WEST]),
    "F": set([SOUTH, EAST]),
    ".": set(),
}

assert all(
    [all([cell == "S" or cell in TILEMAP.keys() for cell in line]) for line in data]
)

# Find S
SCoords: Optional[Coord] = None
for lineIdx, line in enumerate(data):
    if "S" in line:
        SCoords = (line.index("S"), lineIdx)

assert SCoords


# Find S tile by looking at neighbours
SMatchingNeighbours = set()
if SOUTH in TILEMAP[getTileAt(SCoords[0] + NORTH[0], SCoords[1] + NORTH[1])]:
    SMatchingNeighbours.add(NORTH)
if NORTH in TILEMAP[getTileAt(SCoords[0] + SOUTH[0], SCoords[1] + SOUTH[1])]:
    SMatchingNeighbours.add(SOUTH)
if WEST in TILEMAP[getTileAt(SCoords[0] + EAST[0], SCoords[1] + EAST[1])]:
    SMatchingNeighbours.add(EAST)
if EAST in TILEMAP[getTileAt(SCoords[0] + WEST[0], SCoords[1] + WEST[1])]:
    SMatchingNeighbours.add(WEST)
STile = [key for key in TILEMAP.keys() if TILEMAP[key] == SMatchingNeighbours][0]

TILEMAP["S"] = SMatchingNeighbours  # hack to make life easier

# Explore the loop


def getNeighbours(x, y) -> set[Coord]:
    tile = getTileAt(x, y)
    neighboursRelativeCoords = TILEMAP[tile]
    neighbours: set[Coord] = set(
        [(x + dx, y + dy) for (dx, dy) in neighboursRelativeCoords]
    )
    return neighbours


# We will use this structure to store the loop
loopDict: dict[Coord, set[Coord]] = {
    # sourceCoord: nextCoords
}
# And this one to keep track of distances
distToS: dict[Coord, int] = {SCoords: 0}

# We use a fill algorithm where we explore all available neighbours until there is no more to check

coordsToExplore = [SCoords]
markedCoords = set()  # coords that were already explored
while len(coordsToExplore) > 0:
    curCoord: Coord = coordsToExplore.pop(0)
    x, y = curCoord
    # print("Exploring", x, y, getTileAt(x, y))

    neighbours = getNeighbours(x, y)
    # print("\t Found Neighbours", neighbours)
    matchingNeighbours = set(
        [n for n in neighbours if curCoord in getNeighbours(n[0], n[1])]
    )

    # print("\tFound matching", matchingNeighbours)

    loopDict[curCoord] = matchingNeighbours

    for n in matchingNeighbours:
        if n not in markedCoords and n not in coordsToExplore:
            coordsToExplore.append(n)
            # print("\t\tNew node to explore", n)
        if n not in distToS:
            assert curCoord in distToS
            distToS[n] = distToS[curCoord] + 1
            # print("\t\tat dist", distToS[n])

    markedCoords.add(curCoord)

print("Done")

print("Part 1", max([dist for dist in distToS.values()]))

#
# PART 2
#

# Remove the junk tiles from the input
cleanedData = []
for lineY, line in enumerate(data):
    cleanedLine = "".join(
        [c if (x, lineY) in loopDict.keys() else "." for x, c in enumerate(line)]
    )
    cleanedData.append(cleanedLine)

# Write to file for pretty visualization
with open("inputs/day10_cleaned.txt", "w") as f:
    f.write("\n".join(cleanedData))

# Strategy for Part 2 :
# - Redraw the map in a zoomed version (x3) where pipes have a width of one cell
# - Use a bucket fill algorithm on the outside
# - Count the untouched tiles not in the loop

zoomedData = [
    ["." for _ in range(3 * len(cleanedData[0]))] for _ in range(3 * len(cleanedData))
]

for y, line in enumerate(cleanedData):
    for x, tile in enumerate(line):
        if tile in TILEMAP.keys() and tile != ".":
            zoomX, zoomY = 3 * x + 1, 3 * y + 1
            zoomedData[zoomY][zoomX] = "#"

            if NORTH in TILEMAP[tile]:
                zoomedData[zoomY - 1][zoomX] = "#"
            if SOUTH in TILEMAP[tile]:
                zoomedData[zoomY + 1][zoomX] = "#"
            if WEST in TILEMAP[tile]:
                zoomedData[zoomY][zoomX - 1] = "#"
            if EAST in TILEMAP[tile]:
                zoomedData[zoomY][zoomX + 1] = "#"

# Write to file for pretty visualization
with open("inputs/day10_zoomed.txt", "w") as f:
    f.write("\n".join(["".join(line) for line in zoomedData]))

assert zoomedData[0][0] == "."

# Bucketfill from the outside

bucketFillMarks: set[Coord] = set()
bucketFillQueue: list[Coord] = [(0, 0)]

while len(bucketFillQueue) > 0:
    curCoord: Coord = bucketFillQueue.pop(0)
    bucketFillMarks.add(curCoord)
    # print("bucket fill", len(bucketFillQueue), len(bucketFillMarks), curCoord)

    for direction in [NORTH, EAST, SOUTH, WEST]:
        neighCoord: Coord = (curCoord[0] + direction[0], curCoord[1] + direction[1])
        if 0 <= neighCoord[1] <= len(zoomedData) - 1:
            if 0 <= neighCoord[0] <= len(zoomedData[0]) - 1:
                if zoomedData[neighCoord[1]][neighCoord[0]] == ".":
                    if (
                        neighCoord not in bucketFillQueue
                        and neighCoord not in bucketFillMarks
                    ):
                        bucketFillQueue.append(neighCoord)

# Check each tile from original map to see if it's bucket-filled in the zoomed map
part2Sum = 0
for y, line in enumerate(cleanedData):
    for x, tile in enumerate(line):
        zoomX, zoomY = 3 * x + 1, 3 * y + 1
        if tile == ".":
            if (zoomX, zoomY) not in bucketFillMarks:
                part2Sum += 1

print("Part 2", part2Sum)


# 1692 Too high
