import aoc

data = aoc.getCellsForDay(11)

Coord = tuple[int, int]

# example data
"""
data = [
    [c for c in "...#......"],
    [c for c in ".......#.."],
    [c for c in "#........."],
    [c for c in ".........."],
    [c for c in "......#..."],
    [c for c in ".#........"],
    [c for c in ".........#"],
    [c for c in ".........."],
    [c for c in ".......#.."],
    [c for c in "#...#....."],
]
# """


# Mark empty rows and columns

emptyRowsIdx = set()
emptyColsIdx = set()

for rowIdx, line in enumerate(data):
    line = data[rowIdx]
    if "#" not in line:
        emptyRowsIdx.add(rowIdx)

for colIdx in range(len(data[0])):
    column = [data[rowIdx][colIdx] for rowIdx in range(len(data))]
    if "#" not in column:
        emptyColsIdx.add(colIdx)


# Detect galaxies

galaxiesCoord = set()
for y, line in enumerate(data):
    for x, cell in enumerate(line):
        if cell == "#":
            galaxiesCoord.add((x, y))


# Find shortest paths
def getShortestPaths(expansionValue):
    galaxiesPaths: dict[Coord, dict[Coord, int]] = {}
    for gal in galaxiesCoord:
        galaxiesPaths[gal] = {}
        for gal2 in galaxiesCoord:
            if gal == gal2:
                continue
            if gal2 in galaxiesPaths and gal in galaxiesPaths[gal2]:
                # Only keep one instance of each pair
                continue

            galaxiesPaths[gal][gal2] = abs(gal2[0] - gal[0]) + abs(gal2[1] - gal[1])
            # Add the expanded rows and cols to the value
            directionY = 1 if gal2[1] > gal[1] else -1
            directionX = 1 if gal2[0] > gal[0] else -1
            for rowIdx in range(gal[1], gal2[1] + directionY, directionY):
                if rowIdx in emptyRowsIdx:
                    galaxiesPaths[gal][gal2] += expansionValue
            for colIdx in range(gal[0], gal2[0] + directionX, directionX):
                if colIdx in emptyColsIdx:
                    galaxiesPaths[gal][gal2] += expansionValue
    return galaxiesPaths


# Part 1 - Get sum of paths with expansion value 1
part1Sum = 0
part1ShortestPaths = getShortestPaths(expansionValue=1)
for pathDistances in part1ShortestPaths.values():
    for pathDistance in pathDistances.values():
        part1Sum += pathDistance
print("Part 1", part1Sum)

# Some asserts while we refactor the code
# to include the Part 2 logic

if len(data) == 140:
    assert part1Sum == 9681886

if len(data) == 10:
    assert part1Sum == 374

# Part 2 - Get sum of paths with expansion value 999,999
part2Sum = 0
part2ShortestPaths = getShortestPaths(expansionValue=999999)
for pathDistances in part2ShortestPaths.values():
    for pathDistance in pathDistances.values():
        part2Sum += pathDistance
print("Part 2", part2Sum)
